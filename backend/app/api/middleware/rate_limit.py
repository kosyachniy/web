"""
Rate limiting middleware to prevent abuse and ensure fair usage.
Implements sliding window rate limiting with Redis backend.
"""
import time
import hashlib
from typing import Callable, Optional, Dict, Any
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from app.core import settings, get_logger

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using sliding window algorithm.

    Features:
    - Per-IP rate limiting
    - Per-user rate limiting (when authenticated)
    - Different limits for different endpoint types
    - Redis-backed for distributed deployments
    - Graceful degradation when Redis is unavailable
    """

    def __init__(
        self,
        app,
        default_limit: int = 100,  # requests per minute
        window_seconds: int = 60,
        burst_limit: int = 200,
        skip_paths: Optional[list] = None,
        redis_client: Optional[Any] = None,
    ):
        super().__init__(app)
        self.default_limit = default_limit
        self.window_seconds = window_seconds
        self.burst_limit = burst_limit
        self.skip_paths = skip_paths or ["/health", "/ready", "/metrics"]
        self.redis_client = redis_client

        # In-memory fallback when Redis is not available
        self.memory_store: Dict[str, Dict[str, Any]] = {}

        # Rate limits by endpoint type
        self.endpoint_limits = {
            "auth": 20,      # Authentication endpoints
            "read": 200,     # GET endpoints
            "create": 50,    # POST endpoints
            "update": 30,    # PUT/PATCH endpoints
            "delete": 10,    # DELETE endpoints
            "admin": 100,    # Admin endpoints
            "health_check": 1000,  # Health check endpoints
        }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with rate limiting."""

        # Skip rate limiting for certain paths
        if request.url.path in self.skip_paths:
            return await call_next(request)

        # Get client identifier
        client_id = self._get_client_id(request)
        request_id = getattr(request.state, "request_id", "unknown")

        # Determine rate limit for this request
        limit = self._get_rate_limit(request)

        try:
            # Check rate limit
            is_allowed, remaining, reset_time = await self._check_rate_limit(
                client_id, limit, request
            )

            if not is_allowed:
                logger.warning(
                    "Rate limit exceeded",
                    extra={
                        "request_id": request_id,
                        "client_id": client_id,
                        "path": request.url.path,
                        "method": request.method,
                        "limit": limit,
                        "remaining": remaining,
                    }
                )
                return self._create_rate_limit_response(limit, remaining, reset_time)

            # Process request
            response = await call_next(request)

            # Add rate limit headers to successful responses
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_time)

            return response

        except Exception as e:
            logger.error(
                "Rate limiting error",
                extra={
                    "request_id": request_id,
                    "client_id": client_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                }
            )
            # Continue without rate limiting if there's an error
            return await call_next(request)

    def _get_client_id(self, request: Request) -> str:
        """Get unique client identifier for rate limiting."""

        # Try to get authenticated user ID first
        user_id = None
        if hasattr(request.state, "user_id"):
            user_id = request.state.user_id
        elif "authorization" in request.headers:
            # Extract user ID from token if possible
            try:
                from app.core.security import token_manager
                token = request.headers["authorization"].replace("Bearer ", "")
                user_id = token_manager.get_token_subject(token)
            except Exception:
                pass  # Use IP-based rate limiting

        if user_id and user_id != "unknown":
            return f"user:{user_id}"

        # Fall back to IP-based rate limiting
        client_ip = self._get_client_ip(request)
        return f"ip:{client_ip}"

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address."""
        # Check forwarded headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fallback to direct client IP
        if hasattr(request.client, "host"):
            return request.client.host

        return "unknown"

    def _get_rate_limit(self, request: Request) -> int:
        """Determine rate limit based on endpoint type."""
        path = request.url.path.lower()
        method = request.method.upper()

        # Health check endpoints
        if path in self.skip_paths:
            return self.endpoint_limits["health_check"]

        # Authentication endpoints
        if "/auth/" in path:
            return self.endpoint_limits["auth"]

        # Admin endpoints
        if "/admin/" in path:
            return self.endpoint_limits["admin"]

        # Method-based limits
        if method == "GET":
            return self.endpoint_limits["read"]
        elif method == "POST":
            return self.endpoint_limits["create"]
        elif method in ["PUT", "PATCH"]:
            return self.endpoint_limits["update"]
        elif method == "DELETE":
            return self.endpoint_limits["delete"]

        return self.default_limit

    async def _check_rate_limit(
        self, client_id: str, limit: int, request: Request
    ) -> tuple[bool, int, int]:
        """
        Check if request is within rate limit.

        Returns:
            (is_allowed, remaining_requests, reset_timestamp)
        """
        current_time = int(time.time())
        window_start = current_time - self.window_seconds

        if self.redis_client:
            return await self._check_rate_limit_redis(
                client_id, limit, current_time, window_start
            )
        else:
            return self._check_rate_limit_memory(
                client_id, limit, current_time, window_start
            )

    async def _check_rate_limit_redis(
        self, client_id: str, limit: int, current_time: int, window_start: int
    ) -> tuple[bool, int, int]:
        """Redis-based rate limiting using sliding window."""
        key = f"rate_limit:{client_id}"

        try:
            # Use Redis sorted set for sliding window
            pipeline = self.redis_client.pipeline()

            # Remove old entries
            pipeline.zremrangebyscore(key, 0, window_start)

            # Count current requests in window
            pipeline.zcard(key)

            # Add current request
            pipeline.zadd(key, {str(current_time): current_time})

            # Set expiration
            pipeline.expire(key, self.window_seconds + 10)

            results = await pipeline.execute()
            current_requests = results[1] + 1  # +1 for the request we just added

            is_allowed = current_requests <= limit
            remaining = max(0, limit - current_requests)
            reset_time = current_time + self.window_seconds

            return is_allowed, remaining, reset_time

        except Exception as e:
            logger.error(f"Redis rate limiting error: {e}")
            # Fall back to memory-based rate limiting
            return self._check_rate_limit_memory(
                client_id, limit, current_time, window_start
            )

    def _check_rate_limit_memory(
        self, client_id: str, limit: int, current_time: int, window_start: int
    ) -> tuple[bool, int, int]:
        """Memory-based rate limiting fallback."""

        if client_id not in self.memory_store:
            self.memory_store[client_id] = {"requests": [], "reset_time": current_time + self.window_seconds}

        client_data = self.memory_store[client_id]

        # Remove old requests
        client_data["requests"] = [
            req_time for req_time in client_data["requests"]
            if req_time > window_start
        ]

        # Add current request
        client_data["requests"].append(current_time)

        current_requests = len(client_data["requests"])
        is_allowed = current_requests <= limit
        remaining = max(0, limit - current_requests)
        reset_time = current_time + self.window_seconds

        return is_allowed, remaining, reset_time

    def _create_rate_limit_response(
        self, limit: int, remaining: int, reset_time: int
    ) -> JSONResponse:
        """Create rate limit exceeded response."""
        return JSONResponse(
            status_code=429,
            content={
                "type": "/errors/rate_limit_exceeded",
                "title": "Rate Limit Exceeded",
                "status": 429,
                "detail": f"Rate limit of {limit} requests per minute exceeded",
                "retry_after": reset_time - int(time.time()),
            },
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_time),
                "Retry-After": str(reset_time - int(time.time())),
                "Content-Type": "application/problem+json",
            },
        )