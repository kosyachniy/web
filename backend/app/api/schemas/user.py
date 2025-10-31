"""
User API Schemas

Layer 2: API Schemas (Pydantic DTOs for API contracts).
NOT ORM models, NOT domain entities - pure API DTOs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator

from .base import BaseResponse


class UserCreate(BaseModel):
    """
    Layer 2: User creation request schema.

    API contract for creating new users.
    """

    email: EmailStr = Field(
        description="User email address",
        example="user@example.com"
    )
    username: str = Field(
        min_length=3,
        max_length=50,
        description="Unique username",
        example="johndoe"
    )
    password: str = Field(
        min_length=8,
        description="User password",
        example="SecurePass123!"
    )
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="User full name",
        example="John Doe"
    )
    timezone: str = Field(
        default="UTC",
        description="User timezone",
        example="America/New_York"
    )
    language: str = Field(
        default="en",
        description="Preferred language",
        example="en"
    )

    @validator("username")
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, hyphens, and underscores")
        return v.lower()

    @validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "SecurePass123!",
                "full_name": "John Doe",
                "timezone": "America/New_York",
                "language": "en"
            }
        }


class UserUpdate(BaseModel):
    """
    Layer 2: User update request schema.

    API contract for updating existing users.
    """

    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="User full name",
        example="John Doe"
    )
    timezone: Optional[str] = Field(
        None,
        description="User timezone",
        example="America/New_York"
    )
    language: Optional[str] = Field(
        None,
        description="Preferred language",
        example="en"
    )

    class Config:
        """Allow partial updates."""
        exclude_none = True
        json_schema_extra = {
            "example": {
                "full_name": "John Doe Updated",
                "timezone": "Europe/London",
                "language": "es"
            }
        }


class UserRead(BaseModel):
    """
    Layer 2: User response schema.

    API contract for user data responses.
    """

    id: UUID = Field(description="User identifier")
    email: EmailStr = Field(description="User email address")
    username: str = Field(description="Username")
    full_name: Optional[str] = Field(None, description="User full name")
    status: str = Field(description="User status")
    roles: list[str] = Field(description="User roles (multiple roles supported)")
    is_email_verified: bool = Field(description="Email verification status")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")
    login_count: int = Field(description="Total login count")
    timezone: str = Field(description="User timezone")
    language: str = Field(description="Preferred language")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "status": "active",
                "roles": ["user"],
                "is_email_verified": True,
                "last_login_at": "2023-01-15T10:30:00Z",
                "login_count": 42,
                "timezone": "America/New_York",
                "language": "en",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-15T10:30:00Z"
            }
        }


class UserResponse(BaseResponse):
    """
    Layer 2: User API response wrapper.

    Standardized response format for user operations.
    """

    data: UserRead = Field(description="User data")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "User retrieved successfully",
                "data": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "username": "johndoe",
                    "full_name": "John Doe",
                    "status": "active",
                    "roles": ["user"],
                    "is_email_verified": True,
                    "last_login_at": "2023-01-15T10:30:00Z",
                    "login_count": 42,
                    "timezone": "America/New_York",
                    "language": "en",
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-15T10:30:00Z"
                }
            }
        }


class UserListResponse(BaseResponse):
    """
    Layer 2: User list API response.

    Standardized response format for user list operations.
    """

    data: list[UserRead] = Field(description="List of users")
    total: int = Field(description="Total number of users")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Users retrieved successfully",
                "data": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "email": "user@example.com",
                        "username": "johndoe",
                        "full_name": "John Doe",
                        "status": "active",
                        "roles": ["user"],
                        "is_email_verified": True,
                        "last_login_at": "2023-01-15T10:30:00Z",
                        "login_count": 42,
                        "timezone": "America/New_York",
                        "language": "en",
                        "created_at": "2023-01-01T00:00:00Z",
                        "updated_at": "2023-01-15T10:30:00Z"
                    }
                ],
                "total": 1
            }
        }


class UserDeleteResponse(BaseResponse):
    """
    Layer 2: User deletion response schema.

    Standardized response format for user deletion.
    """

    user_id: UUID = Field(description="Deleted user ID")

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            UUID: str,
        }
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "User deleted successfully",
                "user_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }