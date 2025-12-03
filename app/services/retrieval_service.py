from typing import List
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from flashrank import Ranker, RerankRequest
from app.core.config import settings
from app.core.logging import logger

class RetrievalService:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GOOGLE_API_KEY)
        self.vector_store = Chroma(
            collection_name="agentic_rag",
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_DB_DIR
        )
        # Initialize FlashRank (Tiny but powerful)
        self.ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2", cache_dir="opt")

    def retrieve(self, query: str, k: int = 10) -> List[Document]:
        """
        Retrieves top k documents using vector similarity search.
        """
        logger.info(f"Retrieving top {k} documents for query: {query}")
        docs = self.vector_store.similarity_search(query, k=k)
        return docs

    def rerank(self, query: str, documents: List[Document], top_n: int = 5) -> List[Document]:
        """
        Reranks the retrieved documents using FlashRank.
        """
        if not documents:
            return []

        logger.info(f"Reranking {len(documents)} documents...")
        
        # Prepare data for FlashRank
        passages = [
            {"id": str(i), "text": doc.page_content, "meta": doc.metadata} 
            for i, doc in enumerate(documents)
        ]
        
        rerank_request = RerankRequest(query=query, passages=passages)
        results = self.ranker.rerank(rerank_request)
        
        # Sort by score and take top_n
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]
        
        # Reconstruct Documents
        reranked_docs = []
        for res in results:
            # meta is preserved in 'meta' field of result usually, or we map back
            # FlashRank returns dict with 'id', 'text', 'score', 'meta'
            doc = Document(
                page_content=res["text"],
                metadata=res.get("meta", {})
            )
            reranked_docs.append(doc)
            
        logger.info(f"Reranking complete. Top {len(reranked_docs)} returned.")
        return reranked_docs

retrieval_service = RetrievalService()
