"""
Main API Router

Central router that includes all API sub-routers.
"""

from fastapi import APIRouter

from app.api.v1.router import api_router as v1_router

# Main API router
api_router = APIRouter()

# Include version 1 API
api_router.include_router(v1_router)

# Health check endpoint (unversioned)
@api_router.get("/health", tags=["health"])
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

# API info endpoint
@api_router.get("/info", tags=["info"])
async def api_info():
    """API information endpoint."""
    return {
        "name": "Modern Backend API",
        "version": "0.1.0",
        "description": "Scalable backend with hexagonal architecture",
        "api_versions": ["v1"],
    }
