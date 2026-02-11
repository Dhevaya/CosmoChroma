import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Configuration
    API_TITLE: str = "CosmoChroma API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered skin analysis and beauty recommendation engine"
    DEBUG: bool = True
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
    ]
    
    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/jpg"]
    
    # Image Processing Configuration
    FACE_DETECTION_MIN_CONFIDENCE: float = 0.5
    TARGET_IMAGE_SIZE: tuple = (640, 480)
    
    # Color Analysis Configuration
    LAB_DELTA_E_THRESHOLD: float = 50.0
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent
    DATA_DIR: Path = BASE_DIR / "app" / "data"
    MODELS_DIR: Path = BASE_DIR / "app" / "ml_models"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
