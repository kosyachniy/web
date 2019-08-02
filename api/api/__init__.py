import api.account as account
import api.users as users
import api.feedback as feedback
import api.search as search
import api.posts as posts

import api._error as Error

import time

from mongodb import db
from api._error import ErrorWrong
from api._func import get_language


class API():
	def __init__(self, link_server, link_client, ip_server, ip_client, ip, token=None, language=0, ip_remote=None, socketio=None):
		self.timestamp = time.time()
		self.link_server = link_server
		self.link_client = link_client
		self.ip_server = ip_server
		self.ip_client = ip_client
		# self.socketio = socketio
		self.ip = ip
		self.token = token
		self.language = language

		# Язык

		self.language = get_language(self.language)

		# Определение пользователя

		self.user = {
			'id': 0,
			'admin': 2,
		}

		if token:
			db_filter = {'id': True, '_id': False}
			user_id = db['tokens'].find_one({'token': token}, db_filter)
			if user_id and user_id['id']:
				self.user = db['users'].find_one({'id': user_id['id']})
		
		# IP (случай, когда Веб-приложение делает запросы к IP с того же адреса)

		if ip_remote and ip == self.ip_client:
			self.ip = ip_remote

	def method(self, name, params={}):
		# Убираем лишние отступы

		for i in params:
			if type(params[i]) == str:
				params[i] = params[i].strip()

		# Отслеживание действий

		req = {
			'time': self.timestamp,
			'user': self.user['id'],
			'ip': self.ip,
			'method': name,
			'params': params,
		}

		db['actions'].insert(req)
	
		# Метод API

		try:
			module, method = name.split('.')
			func = getattr(globals()[module], method)
		except:
			raise ErrorWrong('method')
		
		# Запрос

		if self.token:
			params['token'] = self.token

		return func(self, **params)