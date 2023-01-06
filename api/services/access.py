"""
Check access by token
"""

import jwt
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from lib import cfg, report


class AccessMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, jwt, whitelist):
        super().__init__(app)
        self.jwt = jwt
        self.whitelist = whitelist

    async def dispatch(self, request: Request, call_next):
        url = request.url.path[4:]

        # JWT
        if request.method == 'POST' and url not in self.whitelist:
            token = (
                request.cookies.get('Authorization')
                or request.headers.get('Authorization')
            )

            if not token:
                # await report.warning("No token", {
                #     'url': url,
                # })
                return Response(content="Invalid token", status_code=401)

            if ' ' in token:
                token = token.split(' ')[1]
            if not token or token == 'null':
                await report.warning("Invalid token", {
                    'url': url,
                    'token': token,
                })
                return Response(content="Invalid token", status_code=401)

            try:
                token = jwt.decode(token, self.jwt, algorithms='HS256')
            except Exception as e:
                await report.warning("Invalid token", {
                    'url': url,
                    'token': token,
                    'error': e,
                })
                return Response(content="Invalid token", status_code=401)

        return await call_next(request)
