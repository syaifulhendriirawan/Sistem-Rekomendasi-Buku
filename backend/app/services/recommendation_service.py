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
    
    def get_book_details(self, book_title: str) -> dict:
        """
        Get book details (author, year, etc.) from final_rating dataframe.
        """
        self.ensure_loaded()
        details = {
            "title": book_title,
            "image_url": None,
            "author": "Unknown",
            "year": None,
            "publisher": "Unknown"
        }
        
        try:
            # Assuming _final_rating has columns: title, author, year, publisher, image_url
            # Filter by title
            rows = self._final_rating[self._final_rating["title"] == book_title]
            if not rows.empty:
                row = rows.iloc[0]
                details["image_url"] = row.get("image_url")
                # Handle possible column name variations if needed, but assuming standard from previous contexts
                details["author"] = row.get("author", "Unknown Author")
                details["year"] = int(row.get("year")) if "year" in row and pd.notna(row["year"]) else None
                details["publisher"] = row.get("publisher", "Unknown Publisher")
        except Exception as e:
            logger.warning(f"Error fetching details for '{book_title}': {e}")
            
        return details

    def get_book_image_url(self, book_title: str) -> Optional[str]:
        """Wrapper for get_book_details for backward compatibility or simple use."""
        return self.get_book_details(book_title).get("image_url")

    def recommend(
        self,
        book_title: str,
        n_recommendations: int = 5
    ) -> List[RecommendedBook]:
        """
        Get book recommendations based on a given book title.
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
            details = self.get_book_details(recommended_title)
            
            recommendations.append(
                RecommendedBook(
                    title=recommended_title,
                    image_url=details["image_url"],
                    author=details["author"],
                    year=details["year"],
                    publisher=details["publisher"],
                    distance=round(float(distance), 4)
                )
            )
        
        logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations
    
    def search_books(self, query: str, limit: int = 10) -> List[str]:
        """
        Search for books by title (case-insensitive partial match).
        """
        self.ensure_loaded()
        
        query_lower = query.lower()
        matches = [
            title for title in self._book_names
            if query_lower in title.lower()
        ]
        
        return matches[:limit]

    def get_featured_books(self, limit: int = 20) -> List[RecommendedBook]:
        """
        Get a list of featured (random) books with their image URLs.
        """
        self.ensure_loaded()
        
        # Get random indices
        total_books = len(self._book_names)
        random_indices = np.random.choice(total_books, min(limit, total_books), replace=False)
        
        featured_books = []
        for idx in random_indices:
            title = self._book_names[idx]
            details = self.get_book_details(title)
            
            featured_books.append(
                RecommendedBook(
                    title=title,
                    image_url=details["image_url"],
                    author=details["author"],
                    year=details["year"],
                    publisher=details["publisher"],
                    distance=0.0
                )
            )
            
        return featured_books


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
