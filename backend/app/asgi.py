"""
ASGI application entry point for the FastAPI backend.

This module creates and configures the main FastAPI application with:
- Modern lifespan management
- Comprehensive middleware stack
- API routing and error handling
- Security and authentication
- Monitoring and observability
"""
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.router import api_router
from app.api.middleware import setup_middlewares
from app.core import settings, get_logger
from app.core.docs import get_openapi_config
from app.core.errors import setup_error_handlers
from app.core.lifespan import lifespan

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    # Create FastAPI app with modern configuration
    app_config = {
        "title": settings.name,
        "version": settings.version,
        "description": "Modern FastAPI backend with best practices",
        "lifespan": lifespan,  # Modern lifespan management (replaces startup/shutdown events)
        "docs_url": "/docs" if settings.debug else None,
        "redoc_url": "/redoc" if settings.debug else None,
        "openapi_url": "/openapi.json" if settings.debug else None,
        "generate_unique_id_function": lambda route: f"{route.tags[0]}-{route.name}" if route.tags else route.name,
    }

    # Add OpenAPI configuration for production
    if not settings.debug:
        openapi_config = get_openapi_config()
        app_config.update(openapi_config)

    app = FastAPI(**app_config)

    # Set up security middleware first (most restrictive)
    if settings.env == "prod":
        # Trust only specific hosts in production
        trusted_hosts = getattr(settings, 'trusted_hosts', ["localhost", "127.0.0.1"])
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=trusted_hosts
        )
        logger.info("Added TrustedHost middleware", extra={"trusted_hosts": trusted_hosts})

    # Set up all HTTP middleware (CORS, rate limiting, timing, etc.)
    setup_middlewares(app)

    # Set up global error handlers
    setup_error_handlers(app)

    # Include API routers
    app.include_router(api_router)

    # Log application setup completion
    logger.info(
        "FastAPI application created successfully",
        extra={
            "app_name": settings.name,
            "version": settings.version,
            "environment": settings.env,
            "debug": settings.debug,
            "docs_enabled": settings.debug,
        }
    )

    return app


# Create the application instance
app = create_app()


# Health check endpoint for load balancers (at root level)
@app.get("/ping", include_in_schema=False)
async def ping():
    """Simple ping endpoint for load balancer health checks."""
    return {"ping": "pong"}


# Application metadata endpoint
@app.get("/info", include_in_schema=False)
async def app_info():
    """Application information endpoint."""
    return {
        "name": settings.name,
        "version": settings.version,
        "environment": settings.env,
        "status": "running"
    }


if __name__ == "__main__":
    # Development server (not for production use)
    import uvicorn

    logger.info("Starting development server...")
    uvicorn.run(
        "app.asgi:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        reload_dirs=["app"] if settings.debug else None,
        log_level="debug" if settings.debug else "info",
        access_log=True,
        reload_includes=["*.py"] if settings.debug else None,
    )