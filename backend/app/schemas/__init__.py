"""
Pydantic schemas for API request/response validation and serialization.

This module provides comprehensive Pydantic schemas separate from API endpoints:
- Request/response models with validation
- Data transfer objects (DTOs)
- Schema inheritance and composition
- Type conversion and serialization
"""

from .base import *
from .user import *
from .category import *
from .post import *

__all__ = [
    # Base schemas
    "BaseSchema",
    "TimestampSchema",
    "PaginationSchema",
    "PaginatedResponseSchema",

    # User schemas
    "UserCreateSchema",
    "UserUpdateSchema",
    "UserResponseSchema",
    "UserProfileSchema",
    "UserListResponseSchema",
    "PasswordChangeSchema",
    "LoginRequestSchema",
    "TokenResponseSchema",

    # Category schemas
    "CategoryCreateSchema",
    "CategoryUpdateSchema",
    "CategoryResponseSchema",
    "CategoryTreeSchema",
    "CategoryStatsSchema",

    # Post schemas
    "PostCreateSchema",
    "PostUpdateSchema",
    "PostResponseSchema",
    "PostSummarySchema",
    "PostListResponseSchema",
]