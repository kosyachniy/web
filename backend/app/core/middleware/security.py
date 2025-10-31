"""
Security Headers Middleware

Middleware for adding comprehensive security headers to HTTP responses.
"""

from __future__ import annotations

from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all HTTP responses.

    Implements security best practices including HSTS, CSP,
    and other protective headers.
    """

    def __init__(
        self,
        app: Callable,
        hsts_max_age: int = 31536000,
        csp_policy: str = "default-src 'self'",
    ):
        super().__init__(app)
        self.hsts_max_age = hsts_max_age
        self.csp_policy = csp_policy

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and add security headers to response.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain

        Returns:
            HTTP response with security headers
        """
        response = await call_next(request)

        # HSTS (HTTP Strict Transport Security)
        response.headers["Strict-Transport-Security"] = (
            f"max-age={self.hsts_max_age}; includeSubDomains"
        )

        # Content Security Policy
        response.headers["Content-Security-Policy"] = self.csp_policy

        # X-Frame-Options
        response.headers["X-Frame-Options"] = "DENY"

        # X-Content-Type-Options
        response.headers["X-Content-Type-Options"] = "nosniff"

        # X-XSS-Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        return response