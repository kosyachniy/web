"""
API v1 Router

Version 1 API router with all endpoints.
"""

from fastapi import APIRouter

# Import routers from the api layer
from app.api.v1.users import router as users_router
# from .auth import router as auth_router
# from .health import router as health_router

api_router = APIRouter()

# Include sub-routers
api_router.include_router(users_router, tags=["users"])
# api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
# api_router.include_router(health_router, prefix="/health", tags=["health"])

# Placeholder endpoint
@api_router.get("/", tags=["root"])
async def api_v1_root():
    """API v1 root endpoint."""
    return {
        "message": "Backend API v1",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "health": "/health",
        }
    }
