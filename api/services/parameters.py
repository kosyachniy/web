"""
Get request & response parameters
"""

import time

from libdev.dev import check_public_ip
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class ParametersMiddleware(BaseHTTPMiddleware):
    """ Getting parameters middleware """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Whitelist
        if request.method != 'POST':
            request.state.ip = None
            return await call_next(request)

        # Request parameters
        request.state.url = request.url.path[4:]
        request.state.start = time.time()
        locale = request.headers.get('accept-language')
        request.state.locale = (
            'ru'
            if locale and 'ru' in locale.lower()
            else 'en'
        ) # TODO: all locales, detect by browser
        request.state.ip = check_public_ip(request.headers.get('x-real-ip'))
        request.state.user_agent = request.headers.get('user-agent')

        # Call
        response = await call_next(request)

        # Response parameters
        response.headers['X-Process-Time'] = f"{request.state.process_time:.3f}"

        return response
