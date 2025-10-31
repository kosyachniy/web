"""
API Schemas

Layer 2: API Schemas (Pydantic DTOs) - API contracts.
NOT ORM models, NOT domain entities.
"""

from .base import BaseResponse, ErrorResponse, PaginatedResponse
from .user import UserCreate, UserRead, UserUpdate, UserResponse

__all__ = [
    "BaseResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserResponse",
]