"""
Pagination dependencies for FastAPI endpoints.
Provides consistent pagination across all list endpoints.
"""
from typing import Optional, Generic, TypeVar, List
from fastapi import Query
from pydantic import BaseModel, Field

from app.core import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of items to return (1-100)"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of items to skip"
    )

    @property
    def skip(self) -> int:
        """Alias for offset for database queries."""
        return self.offset

    @property
    def page(self) -> int:
        """Calculate page number (1-based)."""
        return (self.offset // self.limit) + 1

    def to_dict(self) -> dict:
        """Convert to dictionary for logging/debugging."""
        return {
            "limit": self.limit,
            "offset": self.offset,
            "page": self.page
        }


class CursorPaginationParams(BaseModel):
    """Cursor-based pagination parameters for better performance on large datasets."""

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of items to return (1-100)"
    )
    cursor: Optional[str] = Field(
        default=None,
        description="Cursor for pagination (usually an ID or timestamp)"
    )
    direction: str = Field(
        default="forward",
        regex="^(forward|backward)$",
        description="Pagination direction: forward or backward"
    )

    def to_dict(self) -> dict:
        """Convert to dictionary for logging/debugging."""
        return {
            "limit": self.limit,
            "cursor": self.cursor,
            "direction": self.direction
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""

    items: List[T] = Field(description="List of items for current page")
    total: int = Field(description="Total number of items")
    limit: int = Field(description="Items per page limit")
    offset: int = Field(description="Number of items skipped")
    has_next: bool = Field(description="Whether there are more items")
    has_prev: bool = Field(description="Whether there are previous items")

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        pagination: PaginationParams
    ) -> "PaginatedResponse[T]":
        """Create paginated response from items and pagination params."""
        has_next = (pagination.offset + pagination.limit) < total
        has_prev = pagination.offset > 0

        return cls(
            items=items,
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
            has_next=has_next,
            has_prev=has_prev
        )

    @property
    def page(self) -> int:
        """Current page number (1-based)."""
        return (self.offset // self.limit) + 1

    @property
    def total_pages(self) -> int:
        """Total number of pages."""
        return (self.total + self.limit - 1) // self.limit


class CursorPaginatedResponse(BaseModel, Generic[T]):
    """Cursor-based paginated response model."""

    items: List[T] = Field(description="List of items for current page")
    limit: int = Field(description="Items per page limit")
    has_next: bool = Field(description="Whether there are more items")
    has_prev: bool = Field(description="Whether there are previous items")
    next_cursor: Optional[str] = Field(description="Cursor for next page")
    prev_cursor: Optional[str] = Field(description="Cursor for previous page")

    @classmethod
    def create(
        cls,
        items: List[T],
        pagination: CursorPaginationParams,
        next_cursor: Optional[str] = None,
        prev_cursor: Optional[str] = None
    ) -> "CursorPaginatedResponse[T]":
        """Create cursor paginated response from items and pagination params."""
        has_next = next_cursor is not None
        has_prev = prev_cursor is not None

        return cls(
            items=items,
            limit=pagination.limit,
            has_next=has_next,
            has_prev=has_prev,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor
        )


def get_pagination_params(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of items to return (1-100)"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of items to skip"
    )
) -> PaginationParams:
    """
    Dependency for extracting pagination parameters from query string.

    Usage:
        @app.get("/items")
        async def list_items(pagination: PaginationParams = Depends(get_pagination_params)):
            # Use pagination.limit and pagination.offset
    """
    params = PaginationParams(limit=limit, offset=offset)
    logger.debug("Pagination params extracted", extra=params.to_dict())
    return params


def get_cursor_pagination_params(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of items to return (1-100)"
    ),
    cursor: Optional[str] = Query(
        default=None,
        description="Cursor for pagination"
    ),
    direction: str = Query(
        default="forward",
        regex="^(forward|backward)$",
        description="Pagination direction: forward or backward"
    )
) -> CursorPaginationParams:
    """
    Dependency for extracting cursor-based pagination parameters.

    Usage:
        @app.get("/items")
        async def list_items(pagination: CursorPaginationParams = Depends(get_cursor_pagination_params)):
            # Use pagination for cursor-based pagination
    """
    params = CursorPaginationParams(limit=limit, cursor=cursor, direction=direction)
    logger.debug("Cursor pagination params extracted", extra=params.to_dict())
    return params


def create_pagination_response(
    items: List[T],
    total: int,
    pagination: PaginationParams
) -> PaginatedResponse[T]:
    """Helper function to create paginated responses."""
    return PaginatedResponse.create(items=items, total=total, pagination=pagination)


def create_cursor_pagination_response(
    items: List[T],
    pagination: CursorPaginationParams,
    next_cursor: Optional[str] = None,
    prev_cursor: Optional[str] = None
) -> CursorPaginatedResponse[T]:
    """Helper function to create cursor paginated responses."""
    return CursorPaginatedResponse.create(
        items=items,
        pagination=pagination,
        next_cursor=next_cursor,
        prev_cursor=prev_cursor
    )