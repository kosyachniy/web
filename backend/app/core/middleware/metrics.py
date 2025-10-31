"""
Metrics Collection Middleware

Middleware for collecting Prometheus metrics from HTTP requests.
"""

from __future__ import annotations

from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware for collecting HTTP request metrics.
    Implementation will be completed with monitoring framework.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with metrics collection."""
        # TODO: Implement metrics collection
        return await call_next(request)