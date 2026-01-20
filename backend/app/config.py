"""
Application configuration using Pydantic Settings.
Centralizes all configuration with environment variable support.
"""
import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # App metadata
    app_name: str = "Book Recommendation API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API settings
    api_prefix: str = "/api"
    
    # CORS settings
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Paths - relative to backend directory
    artifacts_dir: str = "artifacts"
    serialized_objects_dir: str = "artifacts/serialized_objects"
    trained_model_dir: str = "artifacts/trained_model"
    dataset_dir: str = "artifacts/dataset"
    
    # Model settings
    trained_model_name: str = "model.pkl"
    n_recommendations: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @property
    def base_path(self) -> Path:
        """Get the base path for the backend directory."""
        return Path(__file__).parent.parent
    
    @property
    def model_path(self) -> Path:
        """Get the full path to the trained model."""
        return self.base_path / self.trained_model_dir / self.trained_model_name
    
    @property
    def book_names_path(self) -> Path:
        """Get the path to book names pickle file."""
        return self.base_path / self.serialized_objects_dir / "book_names.pkl"
    
    @property
    def book_pivot_path(self) -> Path:
        """Get the path to book pivot pickle file."""
        return self.base_path / self.serialized_objects_dir / "book_pivot.pkl"
    
    @property
    def final_rating_path(self) -> Path:
        """Get the path to final rating pickle file."""
        return self.base_path / self.serialized_objects_dir / "final_rating.pkl"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure settings are only loaded once.
    """
    return Settings()
