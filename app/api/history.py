from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models import User
from app.services.history_service import history_service
from app.api.schemas import ConversationResponse, ConversationDetail, ConversationCreate

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    skip: int = 0, 
    limit: int = 50, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve the current user's conversations with optional pagination.
    
    Returns:
        List[ConversationResponse]: A list of the user's conversations ordered by most recent, constrained by `limit` and offset by `skip`.
    """
    return history_service.get_user_conversations(db, user_id=current_user.id, limit=limit, offset=skip)

@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new conversation for the authenticated user.
    
    Parameters:
        conversation (ConversationCreate): Request model containing the conversation title.
    
    Returns:
        ConversationResponse: The created conversation object.
    """
    return history_service.create_conversation(db, user_id=current_user.id, title=conversation.title)

@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation_details(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve the full history and metadata for a specific conversation.
    
    Parameters:
    	conversation_id (int): ID of the conversation to fetch.
    
    Returns:
    	ConversationDetail: The conversation's full history and metadata.
    
    Raises:
    	HTTPException: 404 if the conversation is not found.
    """
    conversation = history_service.get_conversation(db, conversation_id=conversation_id, user_id=current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete the specified conversation for the current authenticated user.
    
    Parameters:
        conversation_id (int): ID of the conversation to delete.
    
    Raises:
        HTTPException: with status code 404 if the conversation does not exist or cannot be deleted.
    """
    success = history_service.delete_conversation(db, conversation_id=conversation_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return None