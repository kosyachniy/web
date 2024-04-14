import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Histogram


metric_endpoints = Histogram(
    "endpoints",
    "Endpoint requests",
    ["method", "status"],
)


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Monitoring requests middleware"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Whitelist
        if request.method != "POST":
            return await call_next(request)

        response = await call_next(request)

        request.state.process_time = time.time() - request.state.start

        # Monitoring
        # TODO: native methods
        metric_endpoints.labels(request.state.url, response.status_code).observe(
            request.state.process_time
        )

        return response
