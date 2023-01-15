"""
Format response object
"""

import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from consys.errors import BaseError
from prometheus_client import Histogram

from lib import report


metric_endpoints = Histogram(
    'endpoints',
    'Endpoint requests',
    ['method', 'status'],
)


class ResponseMiddleware(BaseHTTPMiddleware):
    """ Response formatting middleware """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        url = request.url.path[4:]

        # Whitelist
        if request.method != 'POST':
            return await call_next(request)

        start = time.time()
        request.state.locale = (
            'ru'
            if 'ru' in request.headers.get('accept-language')
            else 'en'
        ) # FIXME
        request.state.ip = request.headers.get('x-real-ip')
        request.state.user_agent = request.headers.get('user-agent')

        try:
            response = await call_next(request)

        except BaseError as e:
            response = Response(content=str(e.txt), status_code=400)
            status = 400

        # pylint: disable=broad-except
        except Exception as e:
            await report.critical(str(e), error=e)
            response = Response(content=str(e), status_code=500)
            status = 500

        else:
            status = response.status_code

            # Report
            if status not in {200, 401}:
                await report.warning("Non-success response", {
                    'url': url,
                    'status': status,
                })

        if request.method == 'POST':
            process_time = time.time() - start

            # Monitoring
            # TODO: native methods
            metric_endpoints.labels(url, status).observe(process_time)

            # Timing
            response.headers['X-Process-Time'] = f"{process_time:.3f}"

        return response
