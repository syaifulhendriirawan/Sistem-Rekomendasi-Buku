"""
Books API routes - endpoints for book listing and search.
"""
from typing import List, Optional
from fastapi import APIRouter, Query, Depends

from app.services.recommendation_service import (
    RecommendationService,
    get_recommendation_service
)
from app.models.recommendation import RecommendedBook

router = APIRouter(prefix="/books", tags=["Books"])


@router.get(
    "/featured",
    response_model=List[RecommendedBook],
    summary="Get featured books",
    description="Get a list of random featured books with covers."
)
async def get_featured_books(
    limit: int = Query(20, ge=1, le=50, description="Number of books to return"),
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[RecommendedBook]:
    """
    Get a list of featured books.
    
    Args:
        limit: Number of books to return
        
    Returns:
        List of featured books
    """
    return service.get_featured_books(limit)


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


@router.get(
    "/details",
    response_model=RecommendedBook,
    summary="Get book details",
    description="Get details for a specific book."
)
async def get_book_details(
    title: str = Query(..., description="Title of the book"),
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendedBook:
    """Get details for a book."""
    details = service.get_book_details(title)
    if not details["year"]:  # Handle None year
        details["year"] = 0
        
    return RecommendedBook(
        title=details["title"],
        image_url=details["image_url"],
        author=details["author"],
        year=details["year"],
        publisher=details["publisher"],
        distance=0.0
    )
