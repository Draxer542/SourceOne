import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "data/chroma_db")
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")

    # Auth Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LangSmith Observability
    LANGSMITH_TRACING: str = os.getenv("LANGSMITH_TRACING", "true")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "agentic-rag-project")

    class Config:
        env_file = ".env"

settings = Settings()

# Push LangSmith vars into os.environ so langchain-core picks them up
os.environ["LANGSMITH_TRACING"] = settings.LANGSMITH_TRACING
os.environ["LANGSMITH_ENDPOINT"]    = settings.LANGSMITH_ENDPOINT
os.environ["LANGSMITH_API_KEY"]     = settings.LANGSMITH_API_KEY
os.environ["LANGSMITH_PROJECT"]     = settings.LANGSMITH_PROJECT
