"""
HTTP middleware for the FastAPI application.

This module provides all middleware components for request/response processing:
- Request ID generation and correlation
- Request timing and performance monitoring
- CORS handling for cross-origin requests
- Rate limiting to prevent abuse
"""

from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

from .request_id import RequestIDMiddleware
from .timing import TimingMiddleware
from .cors import CustomCORSMiddleware, get_cors_middleware_config
from .rate_limit import RateLimitMiddleware
from app.core import settings, get_logger

logger = get_logger(__name__)


def setup_middlewares(app: FastAPI) -> None:
    """
    Set up all middleware for the FastAPI application.

    Middleware is added in reverse order of execution:
    - Last added = First executed
    - First added = Last executed

    Order of execution:
    1. Rate Limiting (first to check limits)
    2. CORS (handle preflight requests early)
    3. GZip (compress responses)
    4. Timing (measure processing time)
    5. Request ID (add correlation ID)
    """

    # 1. Request ID Middleware (executed last, wraps everything)
    app.add_middleware(
        RequestIDMiddleware,
        header_name="X-Request-ID",
        response_header_name="X-Request-ID"
    )
    logger.info("Added RequestID middleware")

    # 2. Timing Middleware (measure total processing time)
    app.add_middleware(
        TimingMiddleware,
        slow_request_threshold=2.0,  # Log warnings for requests >2s
        add_response_header=True,
        header_name="X-Process-Time"
    )
    logger.info("Added Timing middleware")

    # 3. GZip Middleware (compress responses)
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,  # Only compress responses larger than 1KB
        compresslevel=6     # Balance between compression ratio and speed
    )
    logger.info("Added GZip middleware")

    # 4. CORS Middleware (handle cross-origin requests)
    cors_config = get_cors_middleware_config()
    app.add_middleware(CustomCORSMiddleware, **cors_config)
    logger.info("Added CORS middleware", extra={"config": cors_config})

    # 5. Rate Limiting Middleware (executed first)
    # Only add if not in development or explicitly enabled
    if settings.env != "dev" or getattr(settings, 'enable_rate_limiting', False):
        app.add_middleware(
            RateLimitMiddleware,
            default_limit=settings.rate_limit_per_minute,
            window_seconds=60,
            burst_limit=settings.rate_limit_burst,
            skip_paths=["/health", "/ready", "/metrics", "/docs", "/openapi.json"],
            # Redis client will be injected when Redis infrastructure is implemented
            redis_client=None
        )
        logger.info("Added Rate Limiting middleware", extra={
            "default_limit": settings.rate_limit_per_minute,
            "burst_limit": settings.rate_limit_burst
        })
    else:
        logger.info("Rate limiting disabled for development environment")

    logger.info("All middleware setup completed")


# Export middleware classes for direct usage if needed
__all__ = [
    "setup_middlewares",
    "RequestIDMiddleware",
    "TimingMiddleware",
    "CustomCORSMiddleware",
    "RateLimitMiddleware",
    "get_cors_middleware_config"
]