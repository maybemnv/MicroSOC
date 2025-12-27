from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MicroSOC"
    API_V1_STR: str = "/api/v1"
    # Defaulting to sqlite for immediate usability if postgres isn't up, 
    # but structure is ready for postgres.
    DATABASE_URL: str = "sqlite:///./microsoc.db" 
    GOOGLE_API_KEY: Optional[str] = None
    TWILIO_SID: Optional[str] = None
    TWILIO_TOKEN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()
