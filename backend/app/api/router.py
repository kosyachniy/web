"""
Main API router that combines all endpoint routers.
Provides versioned API structure and consistent routing configuration.
"""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core import settings, get_logger

logger = get_logger(__name__)

# Create the main API router
api_router = APIRouter()


@api_router.get("/", include_in_schema=False)
async def root():
    """Root endpoint providing API information."""
    return {
        "name": settings.name,
        "version": settings.version,
        "environment": settings.env,
        "docs_url": "/docs" if settings.debug else None,
        "status": "healthy",
        "message": "FastAPI backend is running"
    }


@api_router.get("/health", tags=["system"])
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    Returns 200 if the service is healthy.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": settings.name,
            "version": settings.version,
            "environment": settings.env
        }
    )


@api_router.get("/ready", tags=["system"])
async def readiness_check():
    """
    Readiness check endpoint that validates dependencies.
    Returns 200 when the service is ready to handle traffic.
    """
    # TODO: Add actual dependency checks (database, Redis, etc.)
    dependencies = {
        "database": True,  # Will be implemented when database layer is added
        "redis": True,     # Will be implemented when Redis layer is added
        "external_services": True,  # Will be implemented for external service checks
    }

    all_ready = all(dependencies.values())
    status_code = status.HTTP_200_OK if all_ready else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if all_ready else "not_ready",
            "service": settings.name,
            "dependencies": dependencies
        }
    )


# Import and include v1 API router
from app.api.v1 import v1_router

# Include v1 API router
api_router.include_router(v1_router)

logger.info("API router configured successfully")