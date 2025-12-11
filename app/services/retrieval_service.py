from typing import List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from flashrank import Ranker, RerankRequest
from app.core.config import settings
from app.core.logging import logger

class RetrievalService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = Chroma(
            collection_name="agentic_rag",
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_DB_DIR
        )
        # Initialize FlashRank
        self.ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2", cache_dir="opt")
        
        # Initialize Hybrid Search
        self.ensemble_retriever = self._initialize_ensemble_retriever()

    def _initialize_ensemble_retriever(self):
        """
        Initializes the EnsembleRetriever with BM25 and Vector Search.
        """
        try:
            logger.info("Initializing Hybrid Search...")
            
            # 1. Vector Retriever
            vector_retriever = self.vector_store.as_retriever(
                search_kwargs={"k": 10}
            )

            # 2. BM25 Retriever
            # We need to fetch documents to initialize BM25. 
            # Note: For large datasets, fetching all docs is inefficient. 
            # Ideally, maintain a separate proper search index (Elastic/Pinecone).
            # Here, we use a simple get() to fetch what we have.
            existing_docs_data = self.vector_store.get()
            documents = []
            
            # Reconstruct Document objects from Chroma data
            if existing_docs_data and existing_docs_data['documents']:
                for i, text in enumerate(existing_docs_data['documents']):
                    metadata = existing_docs_data['metadatas'][i] if existing_docs_data['metadatas'] else {}
                    documents.append(Document(page_content=text, metadata=metadata))
            
            if not documents:
                logger.warning("No documents found in Vector Store. Hybrid Search will rely on empty BM25.")
                # BM25Retriever requires at least one document to init without error usually, 
                # or we just handle the case where it might be empty.
                bm25_retriever = BM25Retriever.from_texts(["Initial Document"], metadatas=[{}])
                bm25_retriever.k = 10
            else:
                bm25_retriever = BM25Retriever.from_documents(documents)
                bm25_retriever.k = 10

            # 3. Ensemble
            ensemble_retriever = EnsembleRetriever(
                retrievers=[bm25_retriever, vector_retriever],
                weights=[0.5, 0.5] # Equal weight to keyword and semantic
            )
            
            logger.info(f"Hybrid Search Initialized with {len(documents)} documents.")
            return ensemble_retriever
            
        except Exception as e:
            logger.error(f"Failed to initialize Hybrid Search: {e}")
            # Fallback to vector store only if BM25 fails
            return self.vector_store.as_retriever(search_kwargs={"k": 10})

    def retrieve(self, query: str, k: int = 10) -> List[Document]:
        """
        Retrieves top k documents using Hybrid Search (Ensemble).
        """
        logger.info(f"Retrieving documents for query: {query}")
        # Note: k is configured in the retrievers themselves during init, 
        # but we can try toimpose it on the result.
        # Ensemble retriever doesn't take 'k' in invoke directly in all versions, 
        # it relies on constituent retrievers. 
        # We can slice the result.
        
        docs = self.ensemble_retriever.invoke(query)
        return docs[:k]

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
            doc = Document(
                page_content=res["text"],
                metadata=res.get("meta", {})
            )
            reranked_docs.append(doc)
            
        logger.info(f"Reranking complete. Top {len(reranked_docs)} returned.")
        return reranked_docs

    def refresh_index(self):
        """
        Refreshes the ensemble retriever by reloading documents from the vector store.
        This is useful after new documents are ingested.
        """
        logger.info("Refreshing Hybrid Search Index...")
        self.ensemble_retriever = self._initialize_ensemble_retriever()
        logger.info("Hybrid Search Index Refreshed.")

retrieval_service = RetrievalService()
