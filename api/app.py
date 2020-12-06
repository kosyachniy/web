# # Logging

# import logging
# logging.basicConfig(filename='error.log', level=logging.DEBUG)

# Main app

from flask import Flask
app = Flask(__name__)

# CORS

from flask_cors import CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Socket.IO

from flask_socketio import SocketIO
sio = SocketIO(app, async_mode=None)

# Limiter

from flask import request, jsonify
from flask_limiter import Limiter

def get_ip():
	try:
		if 'ip' in request.json:
			return request.json['ip']

	except:
		pass

	return request.remote_addr

limiter = Limiter(
	app,
	key_func=get_ip,
	default_limits=['1000/day', '100/hour', '20/minute']
)

# API

from api import API, Error

## Params
from sets import SERVER, CLIENT


api = API(
	server=SERVER,
	client=CLIENT,
	sio=sio,
)


## Endpoints
@app.route('/', methods=['POST'])
def index():
	x = request.json
	# print(x)

	# All required fields are not specified
	for field in ('method', 'token'):
		if field not in x:
			return jsonify({'error': 2, 'result': 'All required fields are not specified!'})

	# Call API

	req = {}

	try:
		res = api.method(
			x['method'],
			x['params'] if 'params' in x else {},
			ip=x['ip'] if 'ip' in x else request.remote_addr, # Case when a web application makes requests from IP with the same address
			token=x['token'] if 'token' in x else None,
			language=x['language'] if 'language' in x else 'en',
		)

	except Error.BaseError as e:
		req['error'] = e.code
		req['result'] = str(e)

	# except Exception as e:
	# 	req['error'] = 1
	# 	req['result'] = 'Server error'

	else:
		req['error'] = 0

		if res:
			req['result'] = res

	# Response

	return jsonify(req)

@app.route('/fb', methods=['POST'])
@app.route('/fb/', methods=['POST'])
def fb():
	x = request.json

	print(x)

	return jsonify({'qwe': 'asd'})

# Sockets

from flask import request

from api import SOCKET


socket = SOCKET(sio)


# Online users

@sio.on('connect', namespace='/main')
def connect():
	socket.method(
		'account.connect',
		sid=request.sid,
	)

@sio.on('online', namespace='/main')
def online(data):
	socket.method(
		'account.online',
		data,
		sid=request.sid,
	)

@sio.on('disconnect', namespace='/main')
def disconnect():
	socket.method(
		'account.disconnect',
		sid=request.sid,
	)


if __name__ == '__main__':
	sio.run(app, debug=False, log_output=False)