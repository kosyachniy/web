"""
Base API Schemas

Layer 2: Base response schemas and common patterns for API contracts.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

T = TypeVar('T')


class BaseResponse(BaseModel):
    """Base response schema with common fields."""

    success: bool = Field(default=True, description="Operation success status")
    message: str | None = Field(default=None, description="Response message")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_encoders = {
            UUID: str,
        }


class ErrorResponse(BaseResponse):
    """Error response schema."""

    success: bool = Field(default=False, description="Operation success status")
    error_code: str | None = Field(default=None, description="Error code")
    error_details: dict[str, Any] | None = Field(default=None, description="Error details")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""

    items: list[T] = Field(description="List of items")
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    per_page: int = Field(description="Items per page")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_previous: bool = Field(description="Whether there is a previous page")

    class Config:
        """Pydantic configuration."""
        from_attributes = True