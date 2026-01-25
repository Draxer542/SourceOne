from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
import json
from fastapi.responses import StreamingResponse
from app.api.schemas import UploadResponse, QueryRequest, QueryResponse, DocumentResponse
from app.core.logging import logger
from app.models import User
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.api.auth import get_current_user

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
async def upload_files(
    background_tasks: BackgroundTasks, 
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
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
async def query_rag(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Queries the RAG system with History Context.
    """
    logger.info(f"Received query: {request.query}")
    try:
        retrieval_service = get_retrieval_service()
        generation_service = get_generation_service()
        
        # 0. Handle Conversation/History
        history_msgs = []
        conversation_id = request.conversation_id
        
        if conversation_id:
             # Fetch existing conversation
             from app.services.history_service import history_service
             from fastapi.concurrency import run_in_threadpool
             conversation = await run_in_threadpool(history_service.get_conversation, db, conversation_id, current_user.id)
             if conversation:
                 history_msgs = conversation.messages
        else:
             # Create new conversation immediately or wait? 
             # Let's create it now to persist this interaction
             from app.services.history_service import history_service
             from fastapi.concurrency import run_in_threadpool
             # Title is first 30 chars of query
             title = (request.query[:30] + '...') if len(request.query) > 30 else request.query
             new_conv = await run_in_threadpool(history_service.create_conversation, db, current_user.id, title)
             conversation_id = new_conv.id

        # 1. Contextualize Query (if history exists)
        langchain_history = generation_service.format_history(history_msgs)
        standalone_query = await generation_service.contextualize_query(request.query, langchain_history)
        
        # 2. Retrieve (using Standalone Query)
        retrieved_docs = retrieval_service.retrieve(standalone_query)
        
        # 3. Rerank
        reranked_docs = retrieval_service.rerank(standalone_query, retrieved_docs)
        
        # 4. Generate Answer (Original Query or Standalone? usually Original + Docs + System Prompt context is fine, 
        # but LangChain pattern uses Standalone query logic. 
        # For this implementation, we feed proper context.
        # Note: generation_service.generate_answer uses the "context" variable in prompt.
        # We pass original query to prompt usually, as context docs are found via standalone.
        answer = await generation_service.generate_answer(request.query, reranked_docs)
        
        # 5. Persist Interaction
        if conversation_id:
             await run_in_threadpool(history_service.add_message, db, conversation_id, "user", request.query)
             await run_in_threadpool(history_service.add_message, db, conversation_id, "assistant", answer)
        
        # Format response
        source_docs = [
            DocumentResponse(content=doc.page_content, metadata=doc.metadata)
            for doc in reranked_docs
        ]
        
        return QueryResponse(answer=answer, source_documents=source_docs, conversation_id=conversation_id)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query-stream")
async def query_rag_stream(
    request: QueryRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Streams the RAG query response in real-time using Server-Sent Events.
    """
    logger.info(f"Received streaming query: {request.query}")
    
    async def stream_generator():
        try:
            retrieval_service = get_retrieval_service()
            generation_service = get_generation_service()
            from app.services.history_service import history_service
            from fastapi.concurrency import run_in_threadpool
            
            # 0. Handle Conversation/History
            history_msgs = []
            conversation_id = request.conversation_id
            
            if conversation_id:
                 conversation = await run_in_threadpool(history_service.get_conversation, db, conversation_id, current_user.id)
                 if conversation:
                     history_msgs = conversation.messages
            else:
                 title = (request.query[:30] + '...') if len(request.query) > 30 else request.query
                 new_conv = await run_in_threadpool(history_service.create_conversation, db, current_user.id, title)
                 conversation_id = new_conv.id
                 # Send conversation ID as first event
                 data_str = json.dumps({"conversation_id": conversation_id})
                 yield f"event: session\ndata: {data_str}\n\n"

            # 1. Contextualize
            langchain_history = generation_service.format_history(history_msgs)
            logger.info(f"Retrieved {len(history_msgs)} messages from DB for Conversation {conversation_id}")
            standalone_query = await generation_service.contextualize_query(request.query, langchain_history)
            
            # 2. Retrieve
            retrieved_docs = retrieval_service.retrieve(standalone_query)
            
            # 3. Rerank
            reranked_docs = retrieval_service.rerank(standalone_query, retrieved_docs)
            
            # 4. Stream the answer
            full_answer = ""
            async for chunk in generation_service.generate_answer_stream(request.query, reranked_docs):
                full_answer += chunk
                # json.dumps ensures literal \n becomes symbol \n in the string
                data_str = json.dumps(chunk)
                yield f"data: {data_str}\n\n"
            
            # 5. Persist
            if conversation_id:
                 await run_in_threadpool(history_service.add_message, db, conversation_id, "user", request.query)
                 await run_in_threadpool(history_service.add_message, db, conversation_id, "assistant", full_answer)

            # Send sources event
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
