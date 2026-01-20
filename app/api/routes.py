from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import json
from fastapi.responses import StreamingResponse
from app.api.schemas import UploadResponse, QueryRequest, QueryResponse, DocumentResponse
from app.core.logging import logger

router = APIRouter()

# Lazy initialization: services initialized on first use, not module import
_ingestion_service = None
_retrieval_service = None
_generation_service = None

def get_ingestion_service():
    """Lazy-load ingestion service on first use."""
    global _ingestion_service
    if _ingestion_service is None:
        from app.services.ingestion_service import ingestion_service
        _ingestion_service = ingestion_service
    return _ingestion_service

def get_retrieval_service():
    """Lazy-load retrieval service on first use."""
    global _retrieval_service
    if _retrieval_service is None:
        from app.services.retrieval_service import retrieval_service
        _retrieval_service = retrieval_service
    return _retrieval_service

def get_generation_service():
    """Lazy-load generation service on first use."""
    global _generation_service
    if _generation_service is None:
        from app.services.generation_service import generation_service
        _generation_service = generation_service
    return _generation_service

@router.post("/upload", response_model=UploadResponse)
async def upload_files(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    """
    Uploads and processes up to 3 files (PDF, MD, TXT, DOCX).
    Index refresh happens in the background for faster response.
    """
    logger.info("Received upload request.")
    try:
        ingestion_service = get_ingestion_service()
        retrieval_service = get_retrieval_service()
        
        result = await ingestion_service.process_files(files)
        # Schedule index refresh in background to avoid blocking
        background_tasks.add_task(retrieval_service.refresh_index)
        return UploadResponse(message=result["message"])
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Queries the RAG system.
    """
    logger.info(f"Received query: {request.query}")
    try:
        retrieval_service = get_retrieval_service()
        generation_service = get_generation_service()
        
        # 1. Retrieve
        retrieved_docs = retrieval_service.retrieve(request.query)
        
        # 2. Rerank
        reranked_docs = retrieval_service.rerank(request.query, retrieved_docs)
        
        # 3. Generate
        answer = await generation_service.generate_answer(request.query, reranked_docs)
        
        # Format response
        source_docs = [
            DocumentResponse(content=doc.page_content, metadata=doc.metadata)
            for doc in reranked_docs
        ]
        
        return QueryResponse(answer=answer, source_documents=source_docs)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query-stream")
async def query_rag_stream(request: QueryRequest):
    """
    Streams the RAG query response in real-time using Server-Sent Events.
    """
    logger.info(f"Received streaming query: {request.query}")
    
    async def stream_generator():
        try:
            retrieval_service = get_retrieval_service()
            generation_service = get_generation_service()
            
            # 1. Retrieve
            retrieved_docs = retrieval_service.retrieve(request.query)
            
            # 2. Rerank
            reranked_docs = retrieval_service.rerank(request.query, retrieved_docs)
            
            # 3. Stream the answer
            async for chunk in generation_service.generate_answer_stream(request.query, reranked_docs):
                # Send chunk as JSON-encoded SSE event to preserve formatting (newlines, etc.)
                if chunk:
                    # json.dumps ensures literal \n becomes symbol \n in the string, which survives SSE newlines
                    data_str = json.dumps(chunk)
                    yield f"data: {data_str}\n\n"
            
            # Send sources event with citation data
            sources_data = [
                {
                    "source": doc.metadata.get("source", "Unknown"),
                    "page": doc.metadata.get("page", None)
                }
                for doc in reranked_docs
            ]
            yield f"event: sources\ndata: {json.dumps(sources_data)}\n\n"
            
            # Send completion signal
            yield "event: done\ndata: [DONE]\n\n"
            
        except Exception as e:
            logger.error(f"Stream query failed: {e}")
            error_data = json.dumps(f"Error: {str(e)}")
            yield f"data: {error_data}\n\n"
            yield "event: done\ndata: [DONE]\n\n"
    
    return StreamingResponse(stream_generator(), media_type="text/event-stream")
