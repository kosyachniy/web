"""
FastAPI Application Factory

Main application factory with proper lifespan management, middleware setup,
and comprehensive configuration.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import get_settings
from app.core.lifespan import lifespan
from app.api.router import api_router
from app.api.exception_handlers import setup_exception_handlers
from app.core.middleware import (
    CorrelationIDMiddleware,
    SecurityHeadersMiddleware,
    RequestLoggingMiddleware,
    MetricsMiddleware,
    RateLimitMiddleware,
)
# Import individual routers for legacy API compatibility
from app.api.v1.categories import router as categories_router
from app.api.v1.posts import router as posts_router


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    settings = get_settings()

    # Create FastAPI app with lifespan management
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="Backend",
        debug=settings.debug,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
        lifespan=lifespan,
        # OpenAPI configuration
        openapi_tags=[
            {
                "name": "authentication",
                "description": "User authentication and authorization operations",
            },
            {
                "name": "users",
                "description": "User management operations",
            },
            {
                "name": "categories",
                "description": "Category management and browsing operations",
            },
            {
                "name": "posts",
                "description": "Post management and content operations",
            },
            {
                "name": "health",
                "description": "System health and monitoring endpoints",
            },
            {
                "name": "admin",
                "description": "Administrative operations",
            },
        ],
    )

    # Setup exception handlers
    setup_exception_handlers(app)

    # Setup middleware stack (order matters!)
    setup_middleware(app, settings)

    # Include API routers
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    # Include legacy routes at root level for backward compatibility with frontend
    # nginx strips /api/ prefix, so backend receives /posts/get/ not /api/posts/get/
    # Frontend expects /api/posts/get/ which nginx forwards as /posts/get/ to backend
    app.include_router(categories_router, tags=["categories-legacy"])
    app.include_router(posts_router, tags=["posts-legacy"])

    return app


def setup_middleware(app: FastAPI, settings: any) -> None:
    """
    Setup middleware stack in correct order.

    Args:
        app: FastAPI application instance
        settings: Application settings
    """
    # 1. CORS middleware (should be first)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
        max_age=settings.security.cors_max_age,
    )

    # 2. Security headers middleware
    if settings.security.enable_security_headers:
        app.add_middleware(
            SecurityHeadersMiddleware,
            hsts_max_age=settings.security.hsts_max_age,
            csp_policy=settings.security.csp_policy,
        )

    # 3. Trusted host middleware
    if not settings.is_development:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"] if settings.debug else [settings.host],
        )

    # 4. Session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.security.session_secret_key,
        session_cookie=settings.security.session_cookie_name,
        max_age=settings.security.session_expire_seconds,
        same_site=settings.security.session_cookie_samesite,
        https_only=settings.security.session_cookie_secure,
    )

    # 5. Compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # 6. Rate limiting middleware
    if settings.rate_limit_enabled:
        app.add_middleware(
            RateLimitMiddleware,
            default_rate_limit=settings.default_rate_limit,
            storage_type=settings.security.rate_limit_storage,
        )

    # 7. Correlation ID middleware
    app.add_middleware(CorrelationIDMiddleware)

    # 8. Metrics collection middleware
    if settings.enable_metrics:
        app.add_middleware(MetricsMiddleware)

    # 9. Request logging middleware (should be last)
    app.add_middleware(
        RequestLoggingMiddleware,
        log_requests=settings.monitoring.log_requests,
        log_responses=settings.monitoring.log_responses,
        log_request_body=settings.monitoring.log_request_body,
        log_response_body=settings.monitoring.log_response_body,
        max_body_size=settings.monitoring.max_log_body_size,
        mask_sensitive=settings.monitoring.mask_sensitive_data,
        sensitive_fields=settings.monitoring.sensitive_fields,
    )


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        access_log=True,
        use_colors=True,
        log_config=None,  # Use our custom logging
    )
