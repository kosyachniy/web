"""
API Endpoints (Transport level)
"""

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from routes import router
from lib import cfg


app = FastAPI(title=cfg('NAME', 'API'), root_path="/api")
app.include_router(router)

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
    allow_methods=['*'],
    allow_headers=['*'],
)

# Socket.IO
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
asgi = socketio.ASGIApp(sio)

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

# ## JWT
# def token_required(f):
#     @wraps(f)
#     async def decorated(data, request):
#         try:
#             header = request.headers.get('Authorization')

#             if not header:
#                 return await f(data, request)

#             token = header.split(' ')[1]

#             if not token or token == 'null':
#                 return await f(data, request)

#             try:
#                 data.jwt = jwt.decode(token, cfg('jwt'), algorithms='HS256')
#             except Exception as e:
#                 await report.error("Invalid token", {
#                     'token': token,
#                     'error': e,
#                 })
#                 return json.dumps({'message': 'Token is invalid!'}), 403

#             return await f(data, request)

#         except Exception as e:
#             await report.error("JWT handler", {
#                 'data': data,
#                 'error': e,
#             })
#             return await f(data, request)

#     return decorated



# Online users

@sio.on('connect')
async def connect(sid, request, data):
    """ Connect socket """
    # await api.method(
    #     'account.connect',
    #     ip=request['asgi.scope']['client'][0],
    #     socket=sid,
    # )

@sio.on('online')
async def online(sid, data):
    """ Socket about online user """
    # await api.method(
    #     'account.online',
    #     data,
    #     socket=sid,
    # )

@sio.on('disconnect')
async def disconnect(sid):
    """ Disconnect socket """
    # await api.method(
    #     'account.disconnect',
    #     socket=sid,
    # )


app.mount('/ws', asgi)
