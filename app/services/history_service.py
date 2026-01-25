from sqlalchemy.orm import Session
from app.models import Conversation, Message
from app.api.schemas import ConversationCreate, MessageCreate
from typing import List, Optional

class HistoryService:
    def get_user_conversations(self, db: Session, user_id: int, limit: int = 20, offset: int = 0) -> List[Conversation]:
        """
        Retrieve a user's conversations ordered by most recently updated.
        
        Parameters:
            user_id (int): ID of the user whose conversations are returned.
            limit (int): Maximum number of conversations to return.
            offset (int): Number of conversations to skip (for pagination).
        
        Returns:
            List[Conversation]: Conversations belonging to the user ordered by `updated_at` descending.
        """
        return db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit).all()

    def get_conversation(self, db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """
        Retrieve a single conversation belonging to a specific user.
        
        Returns:
            The Conversation matching the given `conversation_id` and `user_id`, or `None` if no match is found.
        """
        return db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()

    def create_conversation(self, db: Session, user_id: int, title: str) -> Conversation:
        """
        Create and persist a new conversation for the specified user.
        
        Parameters:
            user_id (int): ID of the user who will own the conversation.
            title (str): Title of the new conversation.
        
        Returns:
            Conversation: The persisted Conversation instance with database-generated fields populated.
        """
        db_conversation = Conversation(user_id=user_id, title=title)
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        return db_conversation

    def add_message(self, db: Session, conversation_id: int, role: str, content: str) -> Message:
        # Update conversation updated_at
        """
        Add a message to a conversation and update that conversation's last-updated timestamp.
        
        If the referenced conversation exists, its `updated_at` is set to the current UTC time before the message is persisted.
        
        Parameters:
            conversation_id (int): ID of the conversation to append the message to.
            role (str): Role of the message author (e.g., "user", "assistant").
            content (str): The message content.
        
        Returns:
            Message: The newly created and persisted Message instance.
        """
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            from datetime import datetime
            conversation.updated_at = datetime.utcnow()
        
        db_message = Message(conversation_id=conversation_id, role=role, content=content)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    def delete_conversation(self, db: Session, conversation_id: int, user_id: int) -> bool:
        """
        Delete a conversation belonging to a specific user and persist the change.
        
        Parameters:
        	conversation_id (int): ID of the conversation to delete.
        	user_id (int): ID of the user who must own the conversation.
        
        Returns:
        	bool: `True` if the conversation was found and deleted, `False` otherwise. Commits the deletion to the database when performed.
        """
        db_conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()
        if db_conversation:
            db.delete(db_conversation)
            db.commit()
            return True
        return False

# Global instance not needed primarily, as we pass DB session, but helpful pattern
history_service = HistoryService()