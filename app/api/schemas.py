from typing import List, Optional
from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str

class QueryRequest(BaseModel):
    query: str

class DocumentResponse(BaseModel):
    content: str
    metadata: dict

class QueryResponse(BaseModel):
    answer: str
    source_documents: List[DocumentResponse]
