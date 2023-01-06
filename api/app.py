"""
API Endpoints (Transport level)
"""

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from services.response import ResponseMiddleware
from services.access import AccessMiddleware
from lib import cfg


app = FastAPI(title=cfg('NAME', 'API'), root_path='/api')


# Prometheus
@app.on_event('startup')
async def startup():
    """ Application startup event """
    Instrumentator().instrument(app).expose(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type'],
)

# Monitoring
app.add_middleware(ResponseMiddleware)

# JWT
app.add_middleware(
    AccessMiddleware,
    jwt_secret=cfg('jwt'),
    whitelist={
        '/',
        '/account/token/'
    },
)

# Socket.IO
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
asgi = socketio.ASGIApp(sio)
app.mount('/ws', asgi)

# # Limiter

# from flask import request, jsonify
# from flask_limiter import Limiter

# def get_ip():
#     try:
#         if 'ip' in request.json:
#             return request.json['ip']

#     except:
#         pass

#     return request.remote_addr

# limiter = Limiter(
#     app,
#     key_func=get_ip,
#     default_limits=['1000/day', '500/hour', '20/minute']
# )


@app.get("/")
@app.post("/")
async def handler():
    """ Ping """
    return 'OK'


# pylint: disable=wrong-import-order,unused-import,wrong-import-position
import routes
