"""
Pydantic models for Recommendation-related data.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.book import Book


class RecommendationRequest(BaseModel):
    """Request model for getting recommendations."""
    
    book_title: str = Field(..., description="Title of the book to get recommendations for")
    n_recommendations: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of recommendations to return"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "book_title": "1984",
                "n_recommendations": 5
            }
        }


class RecommendedBook(BaseModel):
    """Model for a recommended book with similarity score."""
    
    title: str = Field(..., description="Recommended book title")
    image_url: Optional[str] = Field(None, description="URL to book cover image")
    distance: Optional[float] = Field(None, description="Distance score (lower is more similar)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Animal Farm",
                "image_url": "https://example.com/animal-farm.jpg",
                "distance": 0.15
            }
        }


class RecommendationResponse(BaseModel):
    """Response model for book recommendations."""
    
    query_book: str = Field(..., description="The book that was queried")
    recommendations: List[RecommendedBook] = Field(
        ...,
        description="List of recommended books"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_book": "1984",
                "recommendations": [
                    {
                        "title": "Animal Farm",
                        "image_url": "https://example.com/animal-farm.jpg",
                        "distance": 0.15
                    }
                ]
            }
        }
