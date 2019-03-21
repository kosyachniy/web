from flask import request, jsonify, make_response, current_app
from app import app, LINK

import os
# import time
import re
import requests
import base64
# import random
# import string
# from hashlib import md5

# # MongoDB

# from pymongo import MongoClient
# db = MongoClient()['web']

# # Socket.IO

# from threading import Lock
# from flask_socketio import SocketIO, emit

# socketio = SocketIO(app, async_mode=None)

# thread = None
# thread_lock = Lock()

# Междоменные запросы

from datetime import timedelta
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
				attach_to_all=True, automatic_options=True):
	if methods is not None:
		methods = ', '.join(sorted(x.upper() for x in methods))

	# use str instead of basestring if using Python 3.x
	# if headers is not None and not isinstance(headers, basestring):
	# 	headers = ', '.join(x.upper() for x in headers)

	# # use str instead of basestring if using Python 3.x
	# if not isinstance(origin, basestring):
	# 	origin = ', '.join(origin)

	if isinstance(max_age, timedelta):
		max_age = max_age.total_seconds()

	# Determines which methods are allowed
	def get_methods():
		if methods is not None:
			return methods

		options_resp = current_app.make_default_options_response()
		return options_resp.headers['allow']

	# The decorator function
	def decorator(f):
		# Caries out the actual cross domain code
		def wrapped_function(*args, **kwargs):
			if automatic_options and request.method == 'OPTIONS':
				resp = current_app.make_default_options_response()
			else:
				resp = make_response(f(*args, **kwargs))
			if not attach_to_all and request.method != 'OPTIONS':
				return resp

			h = resp.headers
			h['Access-Control-Allow-Origin'] = origin
			h['Access-Control-Allow-Methods'] = get_methods()
			h['Access-Control-Max-Age'] = str(max_age)
			h['Access-Control-Allow-Credentials'] = 'true'
			h['Access-Control-Allow-Headers'] = \
				"Origin, X-Requested-With, Content-Type, Accept, Authorization"
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp

		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator

# Загрузка изображения

def max_image(url):
	all_files = os.listdir(url)
	last = max([0] + [int(i) for i in all_files if i.isdigit()])
	return last + 1

def load_image(data, url, name=None, form='png', type='base64'):
	# Декодирование Base64

	if type == 'base64':
		data = base64.b64decode(data)

	# Имя файла

	if name:
		name = str(name)

		for i in os.listdir(url):
			if re.search(r'^' + name + '\.', i):
				os.remove(url + '/' + i)
	else:
		name = str(max_image(url))
	
	# Запись

	with open('{}/{}.{}'.format(url, name, form), 'wb') as file:
		file.write(data)
	
	#

	return name

def reimg(s):
	k = 0

	while True:
		x = re.search(r'<img ', s[k:])

		if x:
			st = list(x.span())
			st[1] = st[0] + s[k+st[0]:].index('>')
			vs = ''

			if 'src="' in s[k+st[0]:k+st[1]]:
				if re.search(r'image/.*;', s[k+st[0]:k+st[1]]) and 'base64,' in s[k+st[0]:k+st[1]]:
					start = k + st[0] + s[k+st[0]:].index('base64,') + 7
					stop = start + s[start:].index('"')

					b64 = s[start:stop]
					form = re.search(r'image/.*;', s[k+st[0]:start]).group(0)[6:-1]
					adr = load_image(b64, 'app/static/load', form=form)

					# vs = '<img src="{}static/load/{}.{}">'.format(LINK, adr, form)
					vs = '<img src="/static/load/{}.{}">'.format(adr, form)

				else:
					start = k + re.search(r'src=".*', s[k:]).span()[0] + 5
					stop = start + s[start:].index('"')
					href = s[start:stop]

					if href[:7] == '/static':
						href = LINK + href[1:]

					if href[:4] == 'http':
						b64 = str(base64.b64encode(requests.get(href).content))[2:-1]
						form = href.split('.')[-1]
						if 'latex' in form:
							form = 'png'

						adr = load_image(b64, 'app/static/load', form=form)
						vs = '<img src="/static/load/{}.{}">'.format(adr, form)

			if vs:
				s = s[:k+st[0]] + vs + s[k+st[1]+1:]
				k += st[0] + len(vs)
			else:
				k += st[1]
		else:
			break

	return s

#


@app.route('/', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def process():
	x = request.json
	# timestamp = time.time()

	if x['method'] == 'system.test':
		res = {
			'error': 0,
			'request': x,
		}

		return jsonify(res)
	
	elif x['method'] == 'post.get':
		res = {
			'error': 0,
			'cont': 'Текст текст',
		}

		return jsonify(res)
	
	elif x['method'] == 'image.load':
		res = {
			'error': 0,
			'cont': reimg(x['cont']),
		}

		return jsonify(res)