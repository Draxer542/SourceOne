import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from app.core.logging import logger

_embeddings_instance = None

def get_embeddings():
    """
    Singleton pattern: Returns a shared embeddings instance.
    Initializes on first call only to avoid duplicate model loading and API calls.
    
    NVIDIA embeddings are cached after first initialization to avoid:
    - Redundant API connection overhead
    - Repeated model loading
    """
    global _embeddings_instance
    
    if _embeddings_instance is not None:
        return _embeddings_instance
    
    if not os.environ.get("NVIDIA_API_KEY"):
        raise ValueError(
            "NVIDIA_API_KEY environment variable is not set. "
            "Please set it before calling get_embeddings()."
        )
        
    _embeddings_instance = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")
    logger.info("✅ NVIDIA Embeddings initialized successfully.")
    return _embeddings_instance
