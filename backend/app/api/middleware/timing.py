"""
Request timing middleware for performance monitoring.
Measures request processing time and adds timing headers.
"""
import time
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core import get_logger

logger = get_logger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to measure and log request processing times.

    Features:
    - Measures total request processing time
    - Adds timing information to response headers
    - Logs slow requests for performance monitoring
    - Provides metrics for endpoint performance analysis
    """

    def __init__(
        self,
        app,
        slow_request_threshold: float = 1.0,  # seconds
        add_response_header: bool = True,
        header_name: str = "X-Process-Time"
    ):
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
        self.add_response_header = add_response_header
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with timing measurement."""
        start_time = time.perf_counter()
        request_id = getattr(request.state, "request_id", "unknown")

        try:
            # Process the request
            response = await call_next(request)

            # Calculate processing time
            process_time = time.perf_counter() - start_time

            # Add timing header to response
            if self.add_response_header:
                response.headers[self.header_name] = f"{process_time:.4f}"

            # Log timing information
            self._log_timing(request, process_time, response.status_code, request_id)

            return response

        except Exception as e:
            # Calculate processing time even for errors
            process_time = time.perf_counter() - start_time

            # Log error timing
            logger.error(
                "Request failed with timing",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "process_time": round(process_time, 4),
                    "error": str(e),
                    "error_type": type(e).__name__,
                }
            )
            raise

    def _log_timing(
        self,
        request: Request,
        process_time: float,
        status_code: int,
        request_id: str
    ) -> None:
        """Log timing information with appropriate level based on performance."""

        timing_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "process_time": round(process_time, 4),
            "is_slow": process_time > self.slow_request_threshold,
        }

        # Add endpoint classification for better monitoring
        endpoint_type = self._classify_endpoint(request.url.path, request.method)
        timing_data["endpoint_type"] = endpoint_type

        if process_time > self.slow_request_threshold:
            # Log slow requests as warnings
            logger.warning(
                f"Slow request detected ({process_time:.4f}s)",
                extra=timing_data
            )
        else:
            # Log normal requests as debug
            logger.debug(
                "Request timing",
                extra=timing_data
            )

        # Log performance metrics for specific thresholds
        if process_time > 5.0:
            logger.error("Very slow request (>5s)", extra=timing_data)
        elif process_time > 2.0:
            logger.warning("Slow request (>2s)", extra=timing_data)

    def _classify_endpoint(self, path: str, method: str) -> str:
        """Classify endpoint type for better monitoring grouping."""

        # Health check endpoints
        if path in ["/health", "/ready", "/metrics"]:
            return "health_check"

        # Authentication endpoints
        if "/auth/" in path:
            return "auth"

        # API endpoints by method
        if method == "GET":
            return "read"
        elif method == "POST":
            return "create"
        elif method in ["PUT", "PATCH"]:
            return "update"
        elif method == "DELETE":
            return "delete"

        # Admin endpoints
        if "/admin/" in path:
            return "admin"

        # Default classification
        return "api"