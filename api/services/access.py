"""
Check access by token
"""

import json

import jwt
from fastapi import Request, Response

from lib import cfg, report
from app import app


@app.middleware('http')
async def format_response(request: Request, call_next):
    url = request.url.path[4:]

    # JWT
    if request.method == 'POST' and url != '/':
        header = request.headers.get('Authorization')
        if not header:
            await report.error("No token", {
                'url': url,
            })
            return Response(content="Invalid token", status_code=401)

        token = header.split(' ')[1]
        if not token or token == 'null':
            await report.error("Invalid token", {
                'url': url,
                'token': token,
            })
            return Response(content="Invalid token", status_code=401)

        try:
            token = jwt.decode(token, cfg('jwt'), algorithms='HS256')
        except Exception as e:
            await report.error("Invalid token", {
                'url': url,
                'token': token,
                'error': e,
            })
            return Response(content="Invalid token", status_code=401)

        print(token)
    return await call_next(request)
