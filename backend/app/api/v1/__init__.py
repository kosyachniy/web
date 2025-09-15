"""
API v1 router that combines all v1 endpoint modules.

This module provides the main v1 API router that includes all business domain endpoints:
- Authentication and authorization
- User management
- Posts and content management
- Categories and organization
- Admin functionality
"""
from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .posts import router as posts_router
from .categories import router as categories_router
from .admin import router as admin_router

# Create the main v1 API router
v1_router = APIRouter(prefix="/v1", tags=["v1"])

# Include all endpoint routers
v1_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

v1_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"]
)

v1_router.include_router(
    posts_router,
    prefix="/posts",
    tags=["Posts"]
)

v1_router.include_router(
    categories_router,
    prefix="/categories",
    tags=["Categories"]
)

v1_router.include_router(
    admin_router,
    prefix="/admin",
    tags=["Administration"]
)


@v1_router.get("/", include_in_schema=False)
async def v1_info():
    """API v1 information endpoint."""
    return {
        "version": "1.0",
        "status": "active",
        "endpoints": [
            "/v1/auth/*",
            "/v1/users/*",
            "/v1/posts/*",
            "/v1/categories/*",
            "/v1/admin/*"
        ]
    }