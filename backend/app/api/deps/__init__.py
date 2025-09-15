"""
FastAPI dependencies for the API layer.

This module provides all the dependencies needed for API endpoints:
- Authentication and authorization
- Database session management
- Pagination utilities
- Business service injection
"""

from .auth import (
    get_current_user,
    get_current_user_optional,
    require_permissions,
    require_admin,
    require_moderator,
    require_self_or_admin,
    CurrentUser
)
from .db import get_db_session, get_db_transaction, DBSession
from .pagination import (
    get_pagination_params,
    get_cursor_pagination_params,
    PaginationParams,
    CursorPaginationParams,
    PaginatedResponse,
    CursorPaginatedResponse,
    create_pagination_response,
    create_cursor_pagination_response
)
from .services import (
    get_user_service,
    get_auth_service,
    get_post_service,
    get_billing_service,
    get_admin_service,
    UserService,
    AuthService,
    PostService,
    BillingService,
    AdminService,
    UserServiceDep,
    AuthServiceDep,
    PostServiceDep,
    BillingServiceDep,
    AdminServiceDep
)

__all__ = [
    # Authentication
    "get_current_user",
    "get_current_user_optional",
    "require_permissions",
    "require_admin",
    "require_moderator",
    "require_self_or_admin",
    "CurrentUser",

    # Database
    "get_db_session",
    "get_db_transaction",
    "DBSession",

    # Pagination
    "get_pagination_params",
    "get_cursor_pagination_params",
    "PaginationParams",
    "CursorPaginationParams",
    "PaginatedResponse",
    "CursorPaginatedResponse",
    "create_pagination_response",
    "create_cursor_pagination_response",

    # Services
    "get_user_service",
    "get_auth_service",
    "get_post_service",
    "get_billing_service",
    "get_admin_service",
    "UserService",
    "AuthService",
    "PostService",
    "BillingService",
    "AdminService",
    "UserServiceDep",
    "AuthServiceDep",
    "PostServiceDep",
    "BillingServiceDep",
    "AdminServiceDep",
]