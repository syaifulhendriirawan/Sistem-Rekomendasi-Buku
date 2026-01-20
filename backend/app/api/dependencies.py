"""
API dependencies for dependency injection.
"""
from functools import lru_cache
from app.config import Settings, get_settings


def get_settings_dependency() -> Settings:
    """Dependency for injecting settings into routes."""
    return get_settings()
