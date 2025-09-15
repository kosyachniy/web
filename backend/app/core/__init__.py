"""
Core application components.

This module contains the foundational components of the application:
- Settings and configuration management
- Application lifespan management
- Security utilities (JWT, password hashing)
- Structured logging setup
- Global error handling
- API documentation configuration
"""

from .settings import settings, is_development, is_production, is_testing
from .lifespan import lifespan, add_startup_task, add_shutdown_task
from .security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
    SecurityError,
    InvalidTokenError,
    ExpiredTokenError
)
from .logging import get_logger, get_request_logger, bind_context, unbind_context, clear_context
from .errors import (
    APIError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    ServiceUnavailableError,
    BusinessLogicError
)
from .docs import get_openapi_config, get_openapi_tags

__all__ = [
    # Settings
    "settings",
    "is_development",
    "is_production",
    "is_testing",

    # Lifespan
    "lifespan",
    "add_startup_task",
    "add_shutdown_task",

    # Security
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "hash_password",
    "verify_password",
    "SecurityError",
    "InvalidTokenError",
    "ExpiredTokenError",

    # Logging
    "get_logger",
    "get_request_logger",
    "bind_context",
    "unbind_context",
    "clear_context",

    # Errors
    "APIError",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConflictError",
    "RateLimitError",
    "ServiceUnavailableError",
    "BusinessLogicError",

    # Documentation
    "get_openapi_config",
    "get_openapi_tags",
]