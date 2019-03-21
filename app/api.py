from flask import request, jsonify
from app import app, LINK

import os
# import time
import re
import requests
import base64
# import random
# import string
# from hashlib import md5

# MongoDB

from pymongo import MongoClient
db = MongoClient()['web']

# # Socket.IO

# from threading import Lock
# from flask_socketio import SocketIO, emit

# socketio = SocketIO(app, async_mode=None)

# thread = None
# thread_lock = Lock()

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
					adr = load_image(b64, 'load', form=form)

					# vs = '<img src="{}static/load/{}.{}">'.format(LINK, adr, form)
					vs = '<img src="/load/{}.{}">'.format(adr, form)

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
						vs = '<img src="/load/{}.{}">'.format(adr, form)

			if vs:
				s = s[:k+st[0]] + vs + s[k+st[1]+1:]
				k += st[0] + len(vs)
			else:
				k += st[1]
		else:
			break

	return s

#


@app.route('/post', methods=['GET'])
@app.route('/post/', methods=['GET'])
def post_get():
	x = request.json

	db_condition = {}
	db_filter = {'_id': False}
	post = db['posts'].find_one(db_condition, db_filter)

	res = {
		'error': 0,
		'post': post,
	}

	return jsonify(res)
	
# def process():
# 	x = request.json
# 	# timestamp = time.time()

# 	if x['method'] == 'system.test':
# 		res = {
# 			'error': 0,
# 			'request': x,
# 		}

# 		return jsonify(res)
	
# 	elif x['method'] == 'post.get':
# 		db_condition = {}
# 		db_filter = {'_id': False}
# 		post = db['posts'].find_one(db_condition, db_filter)

# 		res = {
# 			'error': 0,
# 			'post': post,
# 		}

# 		print(res)

# 		return jsonify(res)
	
# 	elif x['method'] == 'image.load':
# 		res = {
# 			'error': 0,
# 			'cont': reimg(x['cont']),
# 		}

# 		return jsonify(res)