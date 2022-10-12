"""
Jobs worker
"""

import asyncio

# import requests
import socketio
# from fastapi import FastAPI

from jobs import background


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
# app = socketio.ASGIApp(sio)


asyncio.run(background(sio))
# app = FastAPI(title='Web app API')


# @app.post('/')
# async def index(data, request):
#     return 'OK'
