# app/core/config.py - SIMPLIFIED VERSION
from typing import List

class Settings:
    # Server
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "rab_dashboard"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Admin
    ADMIN_EMAIL: str = "admin@rab.gov.rw"
    ADMIN_PASSWORD: str = "ChangeThis123!"
    ADMIN_USERNAME: str = "admin"

settings = Settings()