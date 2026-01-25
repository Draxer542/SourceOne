from sqlalchemy.orm import Session
from app.models import Conversation, Message
from app.api.schemas import ConversationCreate, MessageCreate
from typing import List, Optional

class HistoryService:
    def get_user_conversations(self, db: Session, user_id: int, limit: int = 20, offset: int = 0) -> List[Conversation]:
        return db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit).all()

    def get_conversation(self, db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        return db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()

    def create_conversation(self, db: Session, user_id: int, title: str) -> Conversation:
        db_conversation = Conversation(user_id=user_id, title=title)
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        return db_conversation

    def add_message(self, db: Session, conversation_id: int, role: str, content: str) -> Message:
        # Update conversation updated_at
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
