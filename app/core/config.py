import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "data/chroma_db")
    
    class Config:
        env_file = ".env"

settings = Settings()
