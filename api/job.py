"""
Jobs worker
"""

import asyncio

import socketio
from prometheus_client import start_http_server

from jobs import background


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


asyncio.run(background(sio))

start_http_server(5000)
