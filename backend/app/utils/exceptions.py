"""
Custom exceptions for the application.
Provides structured error handling with proper HTTP status codes.
"""
from typing import Any, Optional


class AppException(Exception):
    """Base exception for application errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ModelNotFoundError(AppException):
    """Raised when the ML model is not found."""
    
    def __init__(self, message: str = "Model not found. Please train the model first."):
        super().__init__(message=message, status_code=404)


class BookNotFoundError(AppException):
    """Raised when the requested book is not found."""
    
    def __init__(self, book_name: str):
        super().__init__(
            message=f"Book '{book_name}' not found in the database.",
            status_code=404,
            details={"book_name": book_name}
        )


class DataNotLoadedError(AppException):
    """Raised when required data files are not loaded."""
    
    def __init__(self, file_name: str):
        super().__init__(
            message=f"Required data file '{file_name}' is not loaded.",
            status_code=500,
            details={"file_name": file_name}
        )


class TrainingError(AppException):
    """Raised when model training fails."""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=f"Training failed: {message}",
            status_code=500,
            details=details
        )
