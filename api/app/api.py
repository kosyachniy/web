from flask import request, jsonify
from app import app, SERVER, CLIENT

from api import API, Error


@app.route('/', methods=['POST'])
def index():
	x = request.json
	# print(x) # !

	#  Не указан метод API

	if 'method' not in x:
		return jsonify({'error': 2, 'result': 'Wrong method'})

	# #  Не указаны параметры API

	# if 'params' not in x:
	# 	return jsonify({'error': 3, 'message': 'Wrong params'})

	#

	api = API(
		server=SERVER,
		client=CLIENT,
		# socketio=sio,
		ip=request.remote_addr,
		token=x['token'] if 'token' in x else None,
		language=x['language'] if 'language' in x else 'en',
		ip_remote=x['ip'] if 'ip' in x else None,
	)

	req = {}

	try:
		res = api.method(x['method'], x['params'] if 'params' in x else {})

	# HTTP Codes ?

	except Error.ErrorSpecified as e:
		req['error'] = 4
		req['result'] = str(e)

	except Error.ErrorBusy as e:
		req['error'] = 5
		req['result'] = str(e)

	except Error.ErrorInvalid as e:
		req['error'] = 6
		req['result'] = str(e)

	except Error.ErrorWrong as e:
		req['error'] = 7
		req['result'] = str(e)

	except Error.ErrorUpload as e:
		req['error'] = 8
		req['result'] = str(e)

	except Error.ErrorAccess as e:
		req['error'] = 9
		req['result'] = str(e)

	except Error.ErrorEmpty as e:
		req['error'] = 10
		req['result'] = str(e)

	except Error.ErrorEnough as e:
		req['error'] = 11
		req['result'] = str(e)

	except Error.ErrorBlock as e:
		req['error'] = 12
		req['result'] = str(e)

	except Error.ErrorType as e:
		req['error'] = 13
		req['result'] = str(e)

	except Error.ErrorCount as e:
		req['error'] = 14
		req['result'] = str(e)

	# except Exception as e:
	# 	req['error'] = 1
	# 	req['result'] = 'Server error'

	else:
		req['error'] = 0

		if res:
			req['result'] = res

	return jsonify(req)