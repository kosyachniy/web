"""
CORS middleware configuration for cross-origin requests.
Handles CORS headers and preflight requests with security considerations.
"""
from typing import List, Optional
from starlette.middleware.cors import CORSMiddleware as StarletteCORSMiddleware

from app.core import settings, get_logger

logger = get_logger(__name__)


def get_cors_middleware_config() -> dict:
    """
    Get CORS middleware configuration based on environment settings.

    Returns secure defaults for production and permissive settings for development.
    """

    # Development settings - more permissive
    if settings.env in ["dev", "development"]:
        config = {
            "allow_origins": ["*"],  # Allow all origins in development
            "allow_credentials": True,
            "allow_methods": ["*"],  # Allow all HTTP methods
            "allow_headers": ["*"],  # Allow all headers
            "expose_headers": [
                "X-Request-ID",
                "X-Process-Time",
                "X-Rate-Limit-Remaining",
                "X-Rate-Limit-Reset",
            ],
        }
        logger.info("CORS configured for development (permissive)")

    # Production settings - more restrictive
    else:
        # Get allowed origins from settings, with secure defaults
        allowed_origins = getattr(settings, 'cors_origins', [])

        # If no origins specified, use localhost for safety
        if not allowed_origins or allowed_origins == ["*"]:
            allowed_origins = [
                "http://localhost:3000",  # Common React dev server
                "http://localhost:8080",  # Common Vue dev server
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8080",
            ]
            logger.warning(
                "No CORS origins specified for production, using localhost defaults",
                extra={"allowed_origins": allowed_origins}
            )

        config = {
            "allow_origins": allowed_origins,
            "allow_credentials": True,
            "allow_methods": [
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
                "OPTIONS",
                "HEAD",
            ],
            "allow_headers": [
                "Accept",
                "Accept-Language",
                "Content-Language",
                "Content-Type",
                "Authorization",
                "X-Request-ID",
                "X-Requested-With",
            ],
            "expose_headers": [
                "X-Request-ID",
                "X-Process-Time",
                "X-Rate-Limit-Remaining",
                "X-Rate-Limit-Reset",
            ],
        }
        logger.info(
            "CORS configured for production",
            extra={
                "allowed_origins": allowed_origins,
                "allowed_methods": config["allow_methods"]
            }
        )

    return config


class CustomCORSMiddleware(StarletteCORSMiddleware):
    """
    Custom CORS middleware with additional security features and logging.
    """

    def __init__(self, app, **kwargs):
        # Get configuration
        config = get_cors_middleware_config()
        config.update(kwargs)  # Allow override of default config

        super().__init__(app, **config)

        # Store configuration for logging
        self.config = config

    async def dispatch(self, request, call_next):
        """Override dispatch to add custom logging and security checks."""
        origin = request.headers.get("origin")
        request_id = getattr(request.state, "request_id", "unknown")

        # Log CORS requests
        if origin:
            logger.debug(
                "CORS request received",
                extra={
                    "request_id": request_id,
                    "origin": origin,
                    "method": request.method,
                    "path": request.url.path,
                    "is_preflight": request.method == "OPTIONS",
                }
            )

        try:
            response = await super().dispatch(request, call_next)

            # Log CORS response
            if origin:
                allowed_origin = response.headers.get("Access-Control-Allow-Origin")
                logger.debug(
                    "CORS response sent",
                    extra={
                        "request_id": request_id,
                        "origin": origin,
                        "allowed_origin": allowed_origin,
                        "status_code": response.status_code,
                    }
                )

            return response

        except Exception as e:
            logger.error(
                "CORS middleware error",
                extra={
                    "request_id": request_id,
                    "origin": origin,
                    "error": str(e),
                    "error_type": type(e).__name__,
                }
            )
            raise


def create_cors_middleware(app):
    """
    Factory function to create CORS middleware with appropriate configuration.

    Usage:
        app.add_middleware(create_cors_middleware)
    """
    return CustomCORSMiddleware(app)