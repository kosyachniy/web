"""
Endpoints (Transport level)
"""

# # Logging

# import logging
# logging.basicConfig(filename='error.log', level=logging.DEBUG)
# logging.getLogger('socketio').setLevel(logging.ERROR)
# logging.getLogger('engineio').setLevel(logging.ERROR)
# logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

# Main app

from fastapi import FastAPI, Request, WebSocket
app = FastAPI(title='Web app API')

# CORS

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Socket.IO

import socketio
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

# API
## Libraries
### System
import json

### Local
from api import API, Error

## Params
with open('sets.json', 'r') as file:
    CLIENT = json.loads(file.read())['client']

## Global variables
api = API(
    client=CLIENT,
    sio=sio,
)

## Endpoints
from pydantic import BaseModel

### Main
class Input(BaseModel):
    """ Main endpoint model """

    method: str
    params: dict = {}
    locale: str = 'en'
    token: str = None

@app.post('/')
async def index(data: Input, request: Request):
    """ Main API endpoint """

    # print(data, request.client.host, request.client.port)

    # Call API

    req = {}

    try:
        res = await api.method(
            data.method,
            data.params,
            ip=request.client.host,
            token=data.token,
            language=data.locale,
        )

    except Error.BaseError as error:
        req['error'] = error.code
        req['result'] = str(error)

    # except Exception as error:
    #     req['error'] = 1
    #     req['result'] = 'Server error'

    else:
        req['error'] = 0

        if res is not None:
            req['result'] = res

    # Response

    return req

# ### Facebook bot
# @app.route('/fb', methods=['POST'])
# @app.route('/fb/', methods=['POST'])
# def fb():
#     x = request.json
#     print(x)
#     return jsonify({'qwe': 'asd'})

## Sockets
### Online users

@sio.on('connect')
async def connect(sid, request, data):
    """ Connect socket """

    api.method(
        'account.connect',
        ip=request['asgi.scope']['client'][0],
        sid=sid,
    )

@sio.on('online')
async def online(sid, data):
    """ Socket about online user """

    await api.method(
        'account.online',
        data,
        sid=sid,
    )

@sio.on('disconnect')
async def disconnect(sid):
    """ Disconnect socket """

    await api.method(
        'account.disconnect',
        sid=sid,
    )


app.mount('/', asgi) # ?
