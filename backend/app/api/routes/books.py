"""
Books API routes - endpoints for book listing and search.
"""
from typing import List, Optional
from fastapi import APIRouter, Query, Depends

from app.services.recommendation_service import (
    RecommendationService,
    get_recommendation_service
)

router = APIRouter(prefix="/books", tags=["Books"])


@router.get(
    "",
    response_model=List[str],
    summary="Get all book titles",
    description="Returns a list of all available book titles in the database."
)
async def get_all_books(
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[str]:
    """
    Get all available book titles.
    
    Returns:
        List of book titles
    """
    return service.get_book_names()


@router.get(
    "/search",
    response_model=List[str],
    summary="Search books by title",
    description="Search for books by title with partial matching."
)
async def search_books(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[str]:
    """
    Search for books by title.
    
    Args:
        q: Search query (partial match, case-insensitive)
        limit: Maximum number of results
        
    Returns:
        List of matching book titles
    """
    return service.search_books(q, limit)
