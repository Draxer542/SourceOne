from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router as api_router
from app.api.auth import router as auth_router
from app.core.database import engine, Base
from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for app startup/shutdown.
    Pre-initializes the shared embeddings model on startup.
    """
    logger.info("🚀 Application starting up...")
    
    # Initialize Database Tables
    logger.info("🗄️ Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created.")

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

app.include_router(api_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
from app.api.history import router as history_router
app.include_router(history_router, prefix="/api/v1/history", tags=["History"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
