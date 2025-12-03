from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import logger

app = FastAPI(
    title="Agentic RAG API",
    description="A RAG system with Data Ingestion, Retrieval, and Generation layers.",
    version="1.0.0"
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
