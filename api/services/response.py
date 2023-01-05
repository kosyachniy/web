"""
Format response object
"""

import time

from fastapi import Request, Response
from consys.errors import BaseError
from prometheus_client import Histogram

from lib import report
from app import app


metric_endpoints = Histogram(
    'endpoints',
    'Endpoint requests',
    ['method', 'status'],
)


@app.middleware('http')
async def format_response(request: Request, call_next):
    start = time.time()

    try:
        response = await call_next(request)

    except BaseError as e:
        response = Response(content=str(e.txt), status_code=400)
        status = 400

    # pylint: disable=broad-except
    except Exception as e:
        response = Response(content=str(e.txt), status_code=500)
        await report.critical(str(e), error=e)
        status = 500

    else:
        status = 200

    # Monitoring
    # TODO: native methods
    process_time = time.time() - start
    metric_endpoints.labels(request.url.path[4:], status).observe(process_time)

    response.headers['X-Process-Time'] = f"{process_time:.3f}"
    return response
