# Params
from sets import SERVER, CLIENT

# # Logging

# import logging
# logging.basicConfig(filename='error.log', level=logging.DEBUG)
# logging.getLogger('socketio').setLevel(logging.ERROR)
# logging.getLogger('engineio').setLevel(logging.ERROR)
# logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

# Main app

from flask import Flask
app = Flask(__name__)

# CORS

from flask_cors import CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Socket.IO

from flask_socketio import SocketIO
sio = SocketIO(app, cors_allowed_origins=['http://localhost', CLIENT['link'][:-1]])

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
	default_limits=['1000/day', '500/hour', '20/minute']
)

# API
## Libraries
from api import API, Error

## Global variables
api = API(
	server=SERVER,
	client=CLIENT,
	sio=sio,
)

## Endpoints
### Main
@app.route('/', methods=['POST'])
def index():
	data = request.json
	# print(data)

	# All required fields are not specified
	for field in ('method', 'token'):
		if field not in data:
			return jsonify({'error': 2, 'result': 'All required fields are not specified!'})

	# Call API

	req = {}

	try:
		res = api.method(
			data['method'],
			data['params'] if 'params' in data else {},
			ip=data['ip'] if 'ip' in data else request.remote_addr, # Case when a web application makes requests from IP with the same address
			token=data['token'] if 'token' in data else None,
			language=data['language'] if 'language' in data else 'en',
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

### Facebook bot
@app.route('/fb', methods=['POST'])
@app.route('/fb/', methods=['POST'])
def fb():
	x = request.json

	print(x)

	return jsonify({'qwe': 'asd'})

## Sockets
### Online users

@sio.on('connect', namespace='/main')
def connect():
	api.method(
		'account.connect',
		ip=request.remote_addr,
		sid=request.sid,
	)

@sio.on('online', namespace='/main')
def online(data):
	api.method(
		'account.online',
		data,
		ip=request.remote_addr,
		sid=request.sid,
	)

@sio.on('disconnect', namespace='/main')
def disconnect():
	api.method(
		'account.disconnect',
		ip=request.remote_addr,
		sid=request.sid,
	)


if __name__ == '__main__':
	sio.run(app, debug=False, log_output=False)