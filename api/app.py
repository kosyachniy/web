"""
API Endpoints (Transport level)
"""

import io

import socketio
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from services.response import ResponseMiddleware
from services.access import AccessMiddleware
from lib import cfg, report


app = FastAPI(title=cfg('NAME', 'API'), root_path='/api')


# Prometheus
@app.on_event('startup')
async def startup():
    """ Application startup event """
    if cfg('mode') in {'PRE', 'PROD'}:
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
async def ping():
    """ Ping """
    return 'OK'

@app.post("/upload/")
async def uploader(upload: bytes = File()):
    """ Upload files to file server """

    # pylint: disable=wrong-import-order,wrong-import-position
    from libdev.aws import upload_file

    try:
        url = upload_file(io.BytesIO(upload))
    # pylint: disable=broad-except
    except Exception as e:
        await report.critical("Upload", error=e)

    return {
        'url': url,
    }


# pylint: disable=wrong-import-order,wrong-import-position,unused-import
import routes
