"""
FastAPI Application Entry Point

This is the main entry point for the Book Recommendation API.
It configures the FastAPI app with CORS, routes, and exception handlers.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.api.routes import books, recommendations
from app.services.recommendation_service import get_recommendation_service
from app.utils.logger import logger
from app.utils.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Loads ML artifacts on startup for faster first request.
    """
    logger.info("Starting application...")
    
    # Pre-load ML artifacts on startup
    try:
        service = get_recommendation_service()
        service.load_artifacts()
        logger.info("ML artifacts pre-loaded successfully")
    except Exception as e:
        logger.warning(f"Could not pre-load ML artifacts: {e}")
        logger.warning("Artifacts will be loaded on first request")
    
    yield
    
    logger.info("Shutting down application...")


# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## Book Recommendation API
    
    A collaborative filtering-based book recommendation system using K-Nearest Neighbors.
    
    ### Features:
    - Get personalized book recommendations
    - Search books by title
    - Fast inference with pre-loaded models
    
    ### Algorithm:
    Uses KNN with cosine similarity on a user-book rating matrix to find
    books with similar rating patterns.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for AppException
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details
        }
    )


# Global exception handler for unexpected errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": str(exc) if settings.debug else None
        }
    )


# Health check endpoint
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Check if the API is running and ML model is loaded."
)
async def health_check():
    """
    Health check endpoint for deployment monitoring.
    
    Returns:
        Status of the API and model loading state
    """
    service = get_recommendation_service()
    
    return {
        "status": "healthy",
        "model_loaded": service.is_loaded,
        "version": settings.app_version
    }


# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="API root",
    description="Welcome endpoint with API information."
)
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(books.router, prefix=settings.api_prefix)
app.include_router(recommendations.router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
