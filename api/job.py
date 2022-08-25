"""
Jobs worker
"""

import asyncio

# import requests
import socketio
# from fastapi import FastAPI

from api.lib import cfg
from jobs import background


LINK = cfg('API')


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
# app = socketio.ASGIApp(sio)


# # Online users

# @sio.on('connect')
# async def connect(sid, request, data):
#     """ Connect socket """
#     requests.post(LINK, json={
#         'method': 'account.connect',
#         'socket': sid,
#     })
#     # await api.method(
#     #     'account.connect',
#     #     ip=request['asgi.scope']['client'][0],
#     #     socket=sid,
#     # )

# @sio.on('online')
# async def online(sid, data):
#     """ Socket about online user """
#     requests.post(LINK, json={
#         'method': 'account.online',
#         'params': data,
#         'socket': sid,
#     })
#     # await api.method(
#     #     'account.online',
#     #     data,
#     #     socket=sid,
#     # )

# @sio.on('disconnect')
# async def disconnect(sid):
#     """ Disconnect socket """
#     requests.post(LINK, json={
#         'method': 'account.disconnect',
#         'socket': sid,
#     })
#     # await api.method(
#     #     'account.disconnect',
#     #     socket=sid,
#     # )


asyncio.run(background(sio))
# app = FastAPI(title='Web app API')


# @app.post('/')
# async def index(data, request):
#     return 'OK'
