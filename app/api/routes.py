from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.schemas import UploadResponse, QueryRequest, QueryResponse, DocumentResponse
from app.services.ingestion_service import ingestion_service
from app.services.retrieval_service import retrieval_service
from app.services.generation_service import generation_service
from app.core.logging import logger

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Uploads and processes up to 3 files (PDF, MD, TXT, DOCX).
    """
    logger.info("Received upload request.")
    try:
        result = await ingestion_service.process_files(files)
        # Refresh the retrieval index to include new documents
        retrieval_service.refresh_index()
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
