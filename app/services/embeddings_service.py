import os
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.logging import logger

_embeddings_instance = None

def get_embeddings():
    """
    Singleton pattern: Returns a shared embeddings instance.
    Initializes on first call only to avoid duplicate model loading.
    
    Models are cached locally in the 'opt' directory to avoid re-downloads:
    - sentence-transformers/all-MiniLM-L6-v2: ~90MB
    - Models are downloaded only once, then reused from cache
    """
    global _embeddings_instance
    if _embeddings_instance is None:
        logger.info("Initializing HuggingFace Embeddings (Singleton)...")
        logger.info("ℹ️ Model will be cached in 'opt' folder to speed up subsequent startups")
        
        # Ensure cache directory exists
        os.makedirs("opt", exist_ok=True)
        
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_folder="opt"  # Cache models locally to avoid re-downloads
        )
        logger.info("✅ HuggingFace Embeddings initialized and cached.")
    return _embeddings_instance
