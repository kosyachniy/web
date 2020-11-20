from flask import request, jsonify

from sets import SERVER, CLIENT
from app import app, sio
from api import API, Error


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
	app,
	key_func=get_remote_address,
	default_limits=["200 per day", "50 per hour"]
)


@app.route('/', methods=['POST'])
@limiter.limit("20 per minute")
def index():
	x = request.json
	# print(x)

	# All required fields are not specified

	for field in ('method', 'token'): # 'params', 'language'
		if field not in x:
			return jsonify({'error': 2, 'result': 'All required fields are not specified!'})

	#

	api = API(
		server=SERVER,
		client=CLIENT,
		socketio=sio,
		ip=request.remote_addr,
		token=x['token'] if 'token' in x else None,
		language=x['language'] if 'language' in x else 'en',
		ip_remote=x['ip'] if 'ip' in x else None,
	)

	req = {}

	try:
		res = api.method(x['method'], x['params'] if 'params' in x else {})

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

	return jsonify(req)

@app.route('/fb', methods=['POST'])
@app.route('/fb/', methods=['POST'])
def fb():
	x = request.json

	print(x)

	return jsonify({'qwe': 'asd'})