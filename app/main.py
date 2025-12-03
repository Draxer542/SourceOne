from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import logger

app = FastAPI(
    title="Agentic RAG API",
    description="A RAG system with Data Ingestion, Retrieval, and Generation layers.",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Agentic RAG API. Visit /docs for Swagger UI."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
