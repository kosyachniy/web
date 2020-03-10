import time

from func.mongodb import db
from api._func import get_language
import api._error as Error

import api.account as account
import api.users as users
import api.feedback as feedback
import api.search as search
import api.posts as posts


class API():
	def __init__(self, server, client, ip, socketio=None, token=None, language=0, ip_remote=None):
		self.timestamp = time.time()
		self.server = server
		self.client = client
		self.socketio = socketio
		self.ip = ip
		self.token = token
		self.language = get_language(language)

		# User recognition

		self.user = {
			'id': 0,
			'admin': 2,
		}

		if token:
			db_filter = {'id': True, '_id': False}
			user_id = db['tokens'].find_one({'token': token}, db_filter)

			if user_id and user_id['id']:
				user = db['users'].find_one({'id': user_id['id']})

				if user:
					self.user = user

		# IP (case when a web application makes requests from IP with the same address)

		if ip_remote and ip == self.client['ip']:
			self.ip = ip_remote

	def method(self, name, params={}):
		# Remove extra indentation

		for i in params:
			if type(params[i]) == str:
				params[i] = params[i].strip()

		# Action tracking

		req = {
			'time': self.timestamp,
			'user': self.user['id'],
			'ip': self.ip,
			'method': name,
			'params': params,
		}

		db['actions'].insert_one(req)

		# API method

		try:
			module, method = name.split('.')
			func = getattr(globals()[module], method)
		except:
			raise Error.ErrorWrong('method')

		# Request

		return func(self, **params)