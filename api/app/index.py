from flask import render_template, request, jsonify
from app import app, LINK, IP, LINK_CLIENT, IP_CLIENT

import os
import time
import re

from mongodb import db

from api import API, Error


# # Socket.IO

# from threading import Lock
# from flask_socketio import SocketIO, emit

# async_mode = None
# socketio = SocketIO(app, async_mode=async_mode)

# thread = None
# thread_lock = Lock()




ERROR = [
	'Server error',
	'Wrong method',
	'Wrong params',
]


@app.route('/', methods=['POST'])
def index():
	# req = {
	# 	'method': 'system.test',
	# 	'ip': request.remote_addr,
	# }
	# res = loads(post(request.url, json=req).text)

	# return render_template('index.html',
	# 	cont = res,
	# )

	x = request.json

	#  Не указан метод API

	if 'method' not in x:
		return jsonify({'error': 2, 'message': ERROR[1]})

	# #  Не указаны параметры API

	# if 'params' not in x:
	# 	return jsonify({'error': 3, 'message': ERROR[2]})
	
	#

	api = API(
		# socketio=socketio,
		ip=request.remote_addr,
		token=x['token'] if 'token' in x else None,
		language=x['language'] if 'language' in x else 'en',
		ip_remote=x['ip'] if 'ip' in x else None,
		link_server=LINK,
		ip_server=IP,
		link_client=LINK_CLIENT,
		ip_client=IP_CLIENT,
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
	
	# except Exception as e:
	# 	req['error'] = 1
	# 	req['result'] = 'Server error'

	else:
		req['error'] = 0

		if res:
			req['result'] = res

	return jsonify(req)


# # Socket.IO

# @socketio.on('action', namespace='/space')
# def action(x):
# 	global thread
# 	with thread_lock:
# 		if thread is None:
# 			thread = socketio.start_background_task(target=background_thread)


# 	socketio.emit('action', {
# 		'id': x['id'],
# 	}, namespace='/space')


# if __name__ == '__main__':
# 	socketio.run(app, debug=True)


# def background_thread():
# 	while True:
# 		timestamp = time.time()

# 		time.sleep(15)