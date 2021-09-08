"""
API Endpoints (Transport level)
"""

# pylint: disable=wrong-import-order,wrong-import-position

# Main app
from fastapi import FastAPI, Request
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
import traceback

### External
from pydantic import BaseModel

### Local
from api import API
from api.funcs import report
from api.errors import BaseError

## Params
with open('sets.json', 'r') as file:
    sets = json.loads(file.read())

## Global variables
api = API(
    sio=sio,
    **sets,
)

## Endpoints
### Main
class Input(BaseModel):
    """ Main endpoint model """

    method: str
    params: dict = {}
    network: str = ''
    locale: str = None
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
            network=data.network,
            locale=data.locale,
        )

    except BaseError as e:
        req['error'] = e.code
        req['result'] = str(e)

    except Exception as e:
        req['error'] = 1
        req['result'] = "Server error"

        trace = traceback.extract_tb(e.__traceback__)[-1]
        report.critical(
            "Server error",
            {
                'file': trace.filename,
                'line': trace.lineno,
                'error': str(e),
            },
            error=e,
        )

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
        socket=sid,
    )

@sio.on('online')
async def online(sid, data):
    """ Socket about online user """

    await api.method(
        'account.online',
        data,
        socket=sid,
    )

@sio.on('disconnect')
async def disconnect(sid):
    """ Disconnect socket """

    await api.method(
        'account.disconnect',
        socket=sid,
    )


app.mount('/', asgi) # TODO: check it
