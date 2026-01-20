"""
Pydantic models for Book-related data.
"""
from pydantic import BaseModel, Field
from typing import Optional


class Book(BaseModel):
    """Book model with essential metadata."""
    
    title: str = Field(..., description="Book title")
    author: Optional[str] = Field(None, description="Book author")
    year: Optional[str] = Field(None, description="Year of publication")
    publisher: Optional[str] = Field(None, description="Publisher name")
    image_url: Optional[str] = Field(None, description="URL to book cover image")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "1984",
                "author": "George Orwell",
                "year": "1949",
                "publisher": "Secker & Warburg",
                "image_url": "https://example.com/1984.jpg"
            }
        }


class BookTitle(BaseModel):
    """Simple model for book title listing."""
    
    title: str = Field(..., description="Book title")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "1984"
            }
        }
