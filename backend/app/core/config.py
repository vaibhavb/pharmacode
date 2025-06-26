import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PharmaCode"
    API_V1_STR: str = "/api/v1"
    
    ALPHAGENOME_API_KEY: str = os.getenv("ALPHAGENOME_API_KEY", "")
    
    # Rate limiting
    RATE_LIMIT_CALLS: int = 5
    RATE_LIMIT_WINDOW: int = 60
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        case_sensitive = True

settings = Settings()
