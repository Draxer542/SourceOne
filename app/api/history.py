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
    Get all conversations for the current user.
    """
    return history_service.get_user_conversations(db, user_id=current_user.id, limit=limit, offset=skip)

@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new conversation manually.
    """
    return history_service.create_conversation(db, user_id=current_user.id, title=conversation.title)

@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation_details(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get full history of a specific conversation.
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
    Delete a conversation.
    """
    success = history_service.delete_conversation(db, conversation_id=conversation_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return None
