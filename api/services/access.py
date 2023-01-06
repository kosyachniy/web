"""
Check access by token
"""

import jwt
from fastapi import Request, Response

from lib import cfg, report
from app import app


WHITELIST = {
    '/',
    '/account/token/'
}


@app.middleware('http')
async def format_response(request: Request, call_next):
    url = request.url.path[4:]

    # JWT
    if request.method == 'POST' and url not in WHITELIST:
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
            token = jwt.decode(token, cfg('jwt'), algorithms='HS256')
        except Exception as e:
            await report.warning("Invalid token", {
                'url': url,
                'token': token,
                'error': e,
            })
            return Response(content="Invalid token", status_code=401)

    return await call_next(request)
