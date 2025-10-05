"""
Correlation ID Middleware

Middleware for tracking request correlation across distributed systems
and maintaining context throughout request lifecycle.
"""

from __future__ import annotations

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging.correlation import (
    set_correlation_id,
    set_request_id,
    get_or_create_correlation_id,
    get_or_create_request_id,
    clear_context,
)


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle correlation ID and request ID tracking.

    Extracts correlation ID from headers or generates new ones,
    maintains context throughout request processing.
    """

    def __init__(
        self,
        app: Callable,
        correlation_header: str = "X-Correlation-ID",
        request_id_header: str = "X-Request-ID",
    ):
        super().__init__(app)
        self.correlation_header = correlation_header
        self.request_id_header = request_id_header

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with correlation ID context.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain

        Returns:
            HTTP response with correlation headers
        """
        # Clear any existing context
        clear_context()

        # Extract or generate correlation ID
        correlation_id = (
            request.headers.get(self.correlation_header) or
            get_or_create_correlation_id()
        )
        set_correlation_id(correlation_id)

        # Extract or generate request ID
        request_id = (
            request.headers.get(self.request_id_header) or
            get_or_create_request_id()
        )
        set_request_id(request_id)

        # Store IDs in request state for easy access
        request.state.correlation_id = correlation_id
        request.state.request_id = request_id

        try:
            # Process request
            response = await call_next(request)

            # Add correlation headers to response
            response.headers[self.correlation_header] = correlation_id
            response.headers[self.request_id_header] = request_id

            return response

        finally:
            # Clean up context after request
            clear_context()