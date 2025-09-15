"""
Request ID middleware for request tracing and correlation.
Adds unique request IDs to all HTTP requests for better logging and debugging.
"""
import uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core import get_logger

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add unique request IDs to all incoming requests.

    The request ID is:
    1. Generated as a UUID if not provided in headers
    2. Added to request state for use in dependencies and route handlers
    3. Included in response headers for client-side tracing
    4. Available for structured logging throughout the request lifecycle
    """

    def __init__(
        self,
        app,
        header_name: str = "X-Request-ID",
        response_header_name: str = "X-Request-ID"
    ):
        super().__init__(app)
        self.header_name = header_name
        self.response_header_name = response_header_name

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and add request ID."""

        # Get request ID from header or generate a new one
        request_id = request.headers.get(self.header_name)
        if not request_id:
            request_id = str(uuid.uuid4())

        # Add request ID to request state
        request.state.request_id = request_id

        # Log request start
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "user_agent": request.headers.get("User-Agent"),
                "client_ip": self._get_client_ip(request),
            }
        )

        try:
            # Process the request
            response = await call_next(request)

            # Add request ID to response headers
            response.headers[self.response_header_name] = request_id

            # Log successful response
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "method": request.method,
                    "path": request.url.path,
                }
            )

            return response

        except Exception as e:
            # Log error
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                exc_info=True
            )
            raise

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request headers."""
        # Check common headers for client IP (in order of preference)
        ip_headers = [
            "X-Forwarded-For",
            "X-Real-IP",
            "X-Client-IP",
            "CF-Connecting-IP",  # Cloudflare
        ]

        for header in ip_headers:
            if header in request.headers:
                # X-Forwarded-For can contain multiple IPs, take the first one
                ip = request.headers[header].split(",")[0].strip()
                if ip:
                    return ip

        # Fallback to direct client address
        if hasattr(request.client, "host"):
            return request.client.host

        return "unknown"