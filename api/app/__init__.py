# Logging

# import logging
# logging.basicConfig(filename='error.log', level=logging.DEBUG)

# Main app

from flask import Flask
app = Flask(__name__)
# app.config.from_object('config')

# CORS

from flask_cors import CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Socket.IO

from flask_socketio import SocketIO
sio = SocketIO(app, async_mode=None)

# API

from app import api
from app import sockets