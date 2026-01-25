from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, field_validator

class UploadResponse(BaseModel):
    message: str

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[int] = None

class DocumentResponse(BaseModel):
    content: str
    metadata: dict

class QueryResponse(BaseModel):
    answer: str
    source_documents: List[DocumentResponse]
    conversation_id: Optional[int] = None

class UserCreate(BaseModel):
    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, v):
        # Basic regex for email validation to avoid external dependency if possible
        """
        Validate that an email address string has a basic valid format.
        
        Parameters:
            cls (type): The model class.
            v (str): The email address to validate.
        
        Returns:
            str: The original email string if it passes validation.
        
        Raises:
            ValueError: If `v` does not match a basic email address pattern.
        """
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('Invalid email address')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        """
        Validate that a password meets the minimum length requirement.
        
        Parameters:
            v (str): The candidate password to validate.
        
        Returns:
            str: The validated password.
        
        Raises:
            ValueError: If `v` is shorter than 8 characters.
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Optional: Add complexity checks (e.g. number, uppercase)
        # if not any(char.isdigit() for char in v): ...
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Chat History Schemas
class MessageBase(BaseModel):
    role: str
    content: str
class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ConversationDetail(ConversationResponse):
    messages: List[MessageResponse]
