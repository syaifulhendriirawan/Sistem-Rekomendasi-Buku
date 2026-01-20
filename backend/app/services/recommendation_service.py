"""
Recommendation Service - Core business logic for book recommendations.
Handles model loading, inference, and recommendation generation.
"""
import pickle
from pathlib import Path
from typing import List, Tuple, Optional
from functools import lru_cache

import numpy as np
import pandas as pd

from app.config import get_settings, Settings
from app.utils.logger import logger
from app.utils.exceptions import (
    ModelNotFoundError,
    BookNotFoundError,
    DataNotLoadedError
)
from app.models.recommendation import RecommendedBook


class RecommendationService:
    """
    Service class for generating book recommendations.
    
    Uses KNN (K-Nearest Neighbors) algorithm trained on user-book ratings
    to find similar books based on collaborative filtering.
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the recommendation service.
        
        Args:
            settings: Application settings (uses default if not provided)
        """
        self.settings = settings or get_settings()
        self._model = None
        self._book_pivot = None
        self._final_rating = None
        self._book_names = None
        self._is_loaded = False
    
    def load_artifacts(self) -> None:
        """
        Load all required ML artifacts (model and data files).
        
        Raises:
            ModelNotFoundError: If model file doesn't exist
            DataNotLoadedError: If data files don't exist
        """
        logger.info("Loading ML artifacts...")
        
        # Check if model exists
        model_path = self.settings.model_path
        if not model_path.exists():
            raise ModelNotFoundError(
                f"Model not found at {model_path}. Run training first."
            )
        
        # Check if data files exist
        required_files = [
            (self.settings.book_pivot_path, "book_pivot.pkl"),
            (self.settings.final_rating_path, "final_rating.pkl"),
            (self.settings.book_names_path, "book_names.pkl"),
        ]
        
        for path, name in required_files:
            if not path.exists():
                raise DataNotLoadedError(name)
        
        # Load model
        with open(model_path, "rb") as f:
            self._model = pickle.load(f)
        logger.info(f"Loaded model from {model_path}")
        
        # Load book pivot table
        with open(self.settings.book_pivot_path, "rb") as f:
            self._book_pivot = pickle.load(f)
        logger.info(f"Loaded book pivot ({self._book_pivot.shape})")
        
        # Load final rating data (for image URLs)
        with open(self.settings.final_rating_path, "rb") as f:
            self._final_rating = pickle.load(f)
        logger.info(f"Loaded final rating ({self._final_rating.shape})")
        
        # Load book names
        with open(self.settings.book_names_path, "rb") as f:
            self._book_names = pickle.load(f)
        logger.info(f"Loaded {len(self._book_names)} book names")
        
        self._is_loaded = True
        logger.info("All ML artifacts loaded successfully")
    
    @property
    def is_loaded(self) -> bool:
        """Check if all artifacts are loaded."""
        return self._is_loaded
    
    def ensure_loaded(self) -> None:
        """Ensure artifacts are loaded, loading them if necessary."""
        if not self._is_loaded:
            self.load_artifacts()
    
    def get_book_names(self) -> List[str]:
        """
        Get list of all available book titles.
        
        Returns:
            List of book titles
        """
        self.ensure_loaded()
        return list(self._book_names)
    
    def get_book_image_url(self, book_title: str) -> Optional[str]:
        """
        Get the image URL for a book title.
        
        Args:
            book_title: Title of the book
            
        Returns:
            Image URL or None if not found
        """
        self.ensure_loaded()
        
        try:
            idx = np.where(self._final_rating["title"] == book_title)[0]
            if len(idx) > 0:
                return self._final_rating.iloc[idx[0]]["image_url"]
        except Exception as e:
            logger.warning(f"Could not find image URL for '{book_title}': {e}")
        
        return None
    
    def recommend(
        self,
        book_title: str,
        n_recommendations: int = 5
    ) -> List[RecommendedBook]:
        """
        Get book recommendations based on a given book title.
        
        Uses KNN algorithm to find books with similar user rating patterns.
        
        Args:
            book_title: Title of the book to base recommendations on
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended books with metadata
            
        Raises:
            BookNotFoundError: If the book title is not in the database
        """
        self.ensure_loaded()
        
        # Find book index in pivot table
        try:
            book_idx = np.where(self._book_pivot.index == book_title)[0][0]
        except IndexError:
            raise BookNotFoundError(book_title)
        
        logger.info(f"Generating recommendations for: '{book_title}'")
        
        # Get KNN neighbors (n+1 because first result is the query book itself)
        book_vector = self._book_pivot.iloc[book_idx, :].values.reshape(1, -1)
        distances, indices = self._model.kneighbors(
            book_vector,
            n_neighbors=n_recommendations + 1
        )
        
        # Build recommendation list (skip first as it's the query book)
        recommendations = []
        for i in range(1, len(indices[0])):
            idx = indices[0][i]
            distance = distances[0][i]
            
            recommended_title = self._book_pivot.index[idx]
            image_url = self.get_book_image_url(recommended_title)
            
            recommendations.append(
                RecommendedBook(
                    title=recommended_title,
                    image_url=image_url,
                    distance=round(float(distance), 4)
                )
            )
        
        logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations
    
    def search_books(self, query: str, limit: int = 10) -> List[str]:
        """
        Search for books by title (case-insensitive partial match).
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching book titles
        """
        self.ensure_loaded()
        
        query_lower = query.lower()
        matches = [
            title for title in self._book_names
            if query_lower in title.lower()
        ]
        
        return matches[:limit]


# Singleton instance for dependency injection
_recommendation_service: Optional[RecommendationService] = None


def get_recommendation_service() -> RecommendationService:
    """
    Get the recommendation service singleton.
    
    This pattern allows for lazy loading and easy testing.
    """
    global _recommendation_service
    
    if _recommendation_service is None:
        _recommendation_service = RecommendationService()
    
    return _recommendation_service
