"""
Check access by token
"""

import jwt
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from lib import report


class AccessMiddleware(BaseHTTPMiddleware):
    """ Access checking middleware """

    def __init__(self, app, jwt_secret, whitelist):
        super().__init__(app)
        self.jwt = jwt_secret
        self.whitelist = whitelist

    async def dispatch(self, request: Request, call_next):
        url = request.url.path[4:]

        # TODO: check current ip with token ip

        # Whitelist
        if request.method != 'POST' or url in self.whitelist:
            request.state.token = None
            request.state.user = 0
            request.state.network = 0
            return await call_next(request)

        # JWT

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
        # pylint: disable=broad-except
        except Exception as e:
            await report.warning("Invalid token", {
                'url': url,
                'token': token,
                'error': e,
            })
            return Response(content="Invalid token", status_code=401)

        request.state.token = token['token']
        request.state.user = token['user']
        request.state.network = token['network']

        # Don't save IP of servers
        if request.state.network in {'tg'}:
            request.state.ip = None

        return await call_next(request)
