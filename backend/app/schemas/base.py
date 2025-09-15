"""
Base Pydantic schemas with common patterns and utilities.

Provides foundational schemas for consistent API structure:
- Base configuration and validation
- Timestamp management
- Pagination patterns
- Common response structures
"""
from datetime import datetime
from typing import Generic, List, Optional, TypeVar, Any, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator


# Type variable for generic pagination
T = TypeVar('T')


class BaseSchema(BaseModel):
    """
    Base schema with common configuration and utilities.

    Provides consistent configuration for all API schemas:
    - JSON serialization with aliases
    - Datetime handling
    - Validation configuration
    """

    model_config = ConfigDict(
        # Use enum values instead of names in JSON
        use_enum_values=True,
        # Validate assignment of new values
        validate_assignment=True,
        # Allow population by field name or alias
        populate_by_name=True,
        # Convert datetime to string in serialization
        json_encoders={
            datetime: lambda dt: dt.strftime('%d.%m.%Y %H:%M:%S') if dt else None
        },
        # Enable JSON schema generation
        json_schema_extra={
            "examples": {}
        }
    )


class TimestampSchema(BaseSchema):
    """
    Schema mixin for timestamp fields.

    Provides consistent timestamp handling across all models.
    """

    created_at: datetime = Field(
        description="Record creation timestamp",
        examples=["15.01.2024 14:30:00"]
    )

    updated_at: datetime = Field(
        description="Record last update timestamp",
        examples=["15.01.2024 16:45:00"]
    )

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def format_timestamps(cls, v: Any) -> str:
        """Format datetime objects to consistent string format."""
        if isinstance(v, datetime):
            return v.strftime('%d.%m.%Y %H:%M:%S')
        return v


class PaginationSchema(BaseSchema):
    """
    Schema for pagination parameters in API requests.

    Provides standardized pagination with offset/limit pattern.
    """

    offset: int = Field(
        default=0,
        ge=0,
        description="Number of records to skip",
        examples=[0, 10, 20]
    )

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of records to return",
        examples=[10, 20, 50]
    )

    @property
    def skip(self) -> int:
        """Alias for offset for SQLAlchemy compatibility."""
        return self.offset


class PaginatedResponseSchema(BaseSchema, Generic[T]):
    """
    Generic schema for paginated API responses.

    Provides consistent pagination response structure across all endpoints.
    """

    items: List[T] = Field(
        description="List of items in current page"
    )

    total: int = Field(
        ge=0,
        description="Total number of items available",
        examples=[0, 25, 150]
    )

    offset: int = Field(
        ge=0,
        description="Number of records skipped",
        examples=[0, 10, 20]
    )

    limit: int = Field(
        ge=1,
        le=100,
        description="Maximum number of records per page",
        examples=[10, 20, 50]
    )

    has_next: bool = Field(
        description="Whether there are more items available"
    )

    has_previous: bool = Field(
        description="Whether there are previous items"
    )

    @property
    def page_count(self) -> int:
        """Calculate total number of pages."""
        if self.total == 0:
            return 0
        return (self.total - 1) // self.limit + 1

    @property
    def current_page(self) -> int:
        """Calculate current page number (1-indexed)."""
        return (self.offset // self.limit) + 1

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        offset: int = 0,
        limit: int = 20
    ) -> "PaginatedResponseSchema[T]":
        """
        Create paginated response from items and metadata.

        Args:
            items: List of items for current page
            total: Total number of items available
            offset: Number of records skipped
            limit: Maximum records per page

        Returns:
            Paginated response schema
        """
        has_next = offset + limit < total
        has_previous = offset > 0

        return cls(
            items=items,
            total=total,
            offset=offset,
            limit=limit,
            has_next=has_next,
            has_previous=has_previous
        )


class ErrorSchema(BaseSchema):
    """
    Schema for API error responses following RFC 7807 Problem Details.

    Provides consistent error structure across all endpoints.
    """

    type: str = Field(
        description="URI reference that identifies the problem type",
        examples=["/errors/validation_error", "/errors/not_found"]
    )

    title: str = Field(
        description="Short, human-readable summary of the problem",
        examples=["Validation Error", "Resource Not Found"]
    )

    status: int = Field(
        ge=100,
        le=599,
        description="HTTP status code",
        examples=[400, 404, 422, 500]
    )

    detail: Optional[str] = Field(
        default=None,
        description="Human-readable explanation specific to this occurrence",
        examples=["The field 'email' is required", "User with ID 123 not found"]
    )

    instance: Optional[str] = Field(
        default=None,
        description="URI reference that identifies the specific occurrence",
        examples=["/api/v1/users/123", "/api/v1/posts"]
    )

    errors: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details (validation errors, etc.)"
    )


class SuccessSchema(BaseSchema):
    """
    Schema for successful API responses without specific data.

    Used for operations that don't return specific data (delete, etc.).
    """

    success: bool = Field(
        default=True,
        description="Operation success status"
    )

    message: str = Field(
        description="Success message",
        examples=["Resource created successfully", "Operation completed"]
    )

    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional response data"
    )


class FilterSchema(BaseSchema):
    """
    Base schema for filtering parameters.

    Provides common filtering patterns for list endpoints.
    """

    search: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Search query string",
        examples=["python", "tutorial", "machine learning"]
    )

    sort_by: Optional[str] = Field(
        default="created_at",
        description="Field to sort by",
        examples=["created_at", "updated_at", "title", "views_count"]
    )

    sort_order: Optional[str] = Field(
        default="desc",
        pattern="^(asc|desc)$",
        description="Sort order (asc or desc)",
        examples=["asc", "desc"]
    )

    @field_validator('sort_order')
    @classmethod
    def validate_sort_order(cls, v: str) -> str:
        """Validate sort order is either 'asc' or 'desc'."""
        if v.lower() not in ('asc', 'desc'):
            raise ValueError('Sort order must be "asc" or "desc"')
        return v.lower()


class DateRangeFilterSchema(BaseSchema):
    """
    Schema for date range filtering.

    Provides consistent date filtering across endpoints.
    """

    date_from: Optional[datetime] = Field(
        default=None,
        description="Start date for filtering (DD.MM.YYYY format)",
        examples=["01.01.2024"]
    )

    date_to: Optional[datetime] = Field(
        default=None,
        description="End date for filtering (DD.MM.YYYY format)",
        examples=["31.12.2024"]
    )

    @field_validator('date_from', 'date_to', mode='before')
    @classmethod
    def parse_date_strings(cls, v: Any) -> Optional[datetime]:
        """Parse date strings in DD.MM.YYYY format."""
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d.%m.%Y')
            except ValueError:
                raise ValueError('Date must be in DD.MM.YYYY format')
        return v

    def validate_date_range(self) -> None:
        """Validate that date_from is before date_to."""
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValueError('Start date must be before end date')


class MetaSchema(BaseSchema):
    """
    Schema for API response metadata.

    Provides additional information about API responses.
    """

    request_id: Optional[str] = Field(
        default=None,
        description="Request correlation ID"
    )

    response_time_ms: Optional[float] = Field(
        default=None,
        ge=0,
        description="Response processing time in milliseconds"
    )

    api_version: str = Field(
        default="1.0",
        description="API version"
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )