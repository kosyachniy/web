from app import app, sio
from flask import request # , session

import os
import time
import re

from sets import IMAGE
from func.mongodb import db
from api._func import other_sessions, online_emit_add, online_user_update, \
					  online_session_close, online_emit_del


# Socket.IO

from threading import Lock
from flask_socketio import emit

thread = None
thread_lock = Lock()


# Reset online users
db['online'].remove()


# Online users

@sio.on('connect', namespace='/main')
def connect():
	# global thread
	# with thread_lock:
	# 	if thread is None:
	# 		thread = sio.start_background_task(target=background_thread)

	print('IN', request.sid)

@sio.on('online', namespace='/main')
def online(x):
	print('ON', request.sid)

	timestamp = time.time()

	# Define user

	db_filter = {
		'_id': False,
		'id': True,
	}

	user_current = db['tokens'].find_one({'token': x['token']}, db_filter)

	if user_current:
		db_filter = {
			'_id': False,
			'id': True,
			'login': True,
			'name': True,
			'surname': True,
			'avatar': True,
			'admin': True,
		}

		user_current = db['users'].find_one({'id': user_current['id']}, db_filter)

	# Online users
	## Emit all users to this user

	# ? Отправлять неавторизованным пользователям информацию об онлайн?

	db_filter = {
		'_id': False,
		'sid': True,
		'id': True,
		'login': True,
		'name': True,
		'surname': True,
		'avatar': True,
		'admin': True,
	}

	users_auth = list(db['online'].find({'login': {'$exists': True}}, db_filter))
	users_all = list(db['online'].find({}, db_filter))
	count = len(set([i['id'] for i in users_all]))

	users_uniq = dict()
	# if user_current and user_current['admin'] > 3: # Full info only for admins
	for i in users_auth:
		if i['id'] not in users_uniq:
			users_uniq[i['id']] = {
				'id': i['id'],
				'login': i['login'],
				'name': i['name'],
				'surname': i['surname'],
				'avatar': IMAGE['link_opt'] + i['avatar'],
			}

	if count:
		sio.emit('online_add', {
			'count': count,
			'users': list(users_uniq.values()),
		}, room=request.sid, namespace='/main')

	## Already online

	already = other_sessions(user_current['id'] if user_current else x['token'])

	## Add to DB

	online = {
		'sid': request.sid,
		'token': x['token'],
		'start': timestamp,
	}

	if user_current:
		online['id'] = user_current['id']
		online['admin'] = user_current['admin']
		online['login'] = user_current['login']
		online['name'] = user_current['name']
		online['surname'] = user_current['surname']
		online['avatar'] = IMAGE['link_opt'] + user_current['avatar']
	else:
		online['id'] = x['token']
		online['admin'] = 2

	db['online'].insert_one(online)

	## Emit this user to all users

	if not already:
		online_emit_add(sio, user_current)

	# # Visits

	# user_id = user_current['id'] if user_current else 0

	# db_condition = {
	# 	'token': x['token'],
	# 	'user': user_id,
	# }

	# utm = db['utms'].find_one(db_condition)

	# if not utm:
	# 	utm = {
	# 		'token': x['token'],
	# 		'user': user_id,
	# 		# 'utm': utm_mark,
	# 		'time': timestamp,
	# 		'steps': [],
	# 	}

	# 	db['utms'].insert_one(utm)

	# | Sessions (sid) |
	# | Tokens (token) |
	# | Users (id) |

	# Определить вкладку (tab - sid)
	# ? Проверка, что токен не скомпрометирован - по ip?

	# # UTM-метки

	# utm_mark = {}
	# params = x['url'].split('?')
	# if len(params) >= 2:
	# 	params = dict(re.findall(r'([^=\&]*)=([^\&]*)', params[1]))
	# 	if 'utm_source' in params and 'utm_medium' in params:
	# 		utm_mark = {
	# 			'source': params['utm_source'],
	# 			'agent': params['utm_medium'],
	# 		}

	# if utm:
	# 	if utm_mark and not utm['utm']:
	# 		utm['utm'] = utm_mark
	# 		db['utms'].save(utm)

	# else:
	# 	utm = {
	# 		'token': x['token'],
	# 		'user': user_id,
	# 		'utm': utm_mark,
	# 		'time': timestamp,
	# 		'steps': [],
	# 	}

	# 	db['utms'].insert_one(utm)

@sio.on('disconnect', namespace='/main')
def disconnect():
	print('OUT', request.sid)

	online = db['online'].find_one({'sid': request.sid})
	if not online:
		return

	# Close session

	online_user_update(online)
	online_session_close(online)
	online_emit_del(sio, online['id'])
#

if __name__ == '__main__':
	sio.run(app, debug=False, log_output=False)


def background_thread():
	while True:
		timestamp = time.time()

        #

		print('!=!')
		# pass

		#

		time.sleep(10)
