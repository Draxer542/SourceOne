import os
from typing import List
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredMarkdownLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.core.config import settings
from app.core.logging import logger
import aiofiles
import tempfile

ALLOWED_EXTENSIONS = {".pdf", ".md", ".txt", ".docx"}
MAX_FILES = 3

class IngestionService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = Chroma(
            collection_name="agentic_rag",
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_DB_DIR
        )

    def validate_files(self, files: List[UploadFile]):
        """
        Validates the number of files and their extensions.
        """
        if len(files) > MAX_FILES:
            raise HTTPException(status_code=400, detail=f"Maximum {MAX_FILES} files allowed.")
        
        for file in files:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail=f"File type {ext} not supported. Allowed: {ALLOWED_EXTENSIONS}")

    async def process_files(self, files: List[UploadFile]):
        """
        Processes uploaded files: saves temporarily, loads, chunks, and indexes.
        """
        self.validate_files(files)
        
        all_documents = []
        
        for file in files:
            logger.info(f"Processing file: {file.filename}")
            
            # Save to temp file
            suffix = os.path.splitext(file.filename)[1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                documents = self._load_document(tmp_path, suffix)
                all_documents.extend(documents)
            finally:
                os.remove(tmp_path)
        
        if not all_documents:
            return {"message": "No content found in files."}

        chunks = self._chunk_documents(all_documents)
        self._index_documents(chunks)
        
        return {"message": f"Successfully processed {len(files)} files into {len(chunks)} chunks."}

    def _load_document(self, file_path: str, extension: str) -> List[Document]:
        """
        Loads a document based on its extension.
        """
        try:
            if extension == ".pdf":
                loader = PyPDFLoader(file_path)
            elif extension == ".docx":
                loader = Docx2txtLoader(file_path)
            elif extension == ".md":
                loader = UnstructuredMarkdownLoader(file_path)
            elif extension == ".txt":
                loader = TextLoader(file_path)
            else:
                return []
            
            return loader.load()
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            raise HTTPException(status_code=500, detail=f"Error loading file: {str(e)}")

    def _chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Chunks documents using Semantic Chunking.
        """
        logger.info("Chunking documents using SemanticChunker...")
        text_splitter = SemanticChunker(self.embeddings)
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks.")
        return chunks

    def _index_documents(self, chunks: List[Document]):
        """
        Indexes chunks into ChromaDB.
        """
        logger.info("Indexing documents into ChromaDB...")
        self.vector_store.add_documents(chunks)
        logger.info("Indexing complete.")

ingestion_service = IngestionService()
