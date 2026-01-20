"""
Recommendations API routes - endpoints for getting book recommendations.
"""
from typing import List
from fastapi import APIRouter, Query, Depends, HTTPException

from app.services.recommendation_service import (
    RecommendationService,
    get_recommendation_service
)
from app.models.recommendation import RecommendationResponse, RecommendedBook
from app.utils.exceptions import BookNotFoundError

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get(
    "",
    response_model=RecommendationResponse,
    summary="Get book recommendations",
    description="Get personalized book recommendations based on a given book title."
)
async def get_recommendations(
    book: str = Query(
        ...,
        min_length=1,
        description="Book title to get recommendations for"
    ),
    n: int = Query(
        5,
        ge=1,
        le=20,
        description="Number of recommendations to return"
    ),
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    """
    Get book recommendations based on collaborative filtering.
    
    The algorithm finds books that have similar user rating patterns
    to the queried book using K-Nearest Neighbors.
    
    Args:
        book: Title of the book to base recommendations on
        n: Number of recommendations to return (1-20)
        
    Returns:
        RecommendationResponse with query book and list of recommendations
        
    Raises:
        404: If the book is not found in the database
    """
    try:
        recommendations = service.recommend(book, n_recommendations=n)
        
        return RecommendationResponse(
            query_book=book,
            recommendations=recommendations
        )
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e.message))
