from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import logger
from app.services.embeddings_service import get_embeddings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for app startup/shutdown.
    Pre-initializes the shared embeddings model on startup.
    """
    logger.info("🚀 Application starting up...")
    # Embeddings model will be lazy-loaded on first request to speed up startup
    logger.info("ℹ️ Embeddings model will be initialized on first use")
    
    yield
    # Cleanup on shutdown
    logger.info("🛑 Application shutting down...")

app = FastAPI(
    title="Agentic RAG API",
    description="A RAG system with Data Ingestion, Retrieval, and Generation layers.",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.include_router(router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
