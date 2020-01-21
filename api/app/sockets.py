from app import app, sio
from flask import request # , session

import os
import time
import re

from func.mongodb import db
# from api._func import reduce_params


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

	# Online users
	## Emit all users to this user

	db_filter = {
		'_id': False,
		'id': True,
		'token': True,
	}

	onlines = list(db['online'].find({}, db_filter))

	users_uniq = dict()
	for i in onlines:
		if i['token'] not in users_uniq: # !
			users_uniq[i['token']] = { # !
				'id': i['token'], # !
			}

	if len(users_uniq):
		sio.emit('online_add', {
			'count': len(users_uniq),
			'users': list(users_uniq.values()),
		}, room=request.sid, namespace='/main')

	## Already online

	already = False

	for online in onlines:
		if online['token'] == x['token']:
			already = True

	## Add to DB

	online = {
		'id': x['token'], # !
		'sid': request.sid,
		'token': x['token'],
		'start': timestamp,
		'time': timestamp,
	}

	db['online'].insert_one(online)

	## Emit this user to all users

	if not already:
		sio.emit('online_add', {
			'count': len(users_uniq)+1,
			'users': [{'id': x['token']}], # !
		}, namespace='/main')

@sio.on('disconnect', namespace='/main')
def disconnect():
	print('OUT', request.sid)

	# Online users
	## Remove from DB

	online = db['online'].find_one({'sid': request.sid})
	if not online:
		return

	token = online['token']

	db['online'].remove(online['_id'])

	## Other sessions of this user

	db_filter = {
		'_id': False,
		'token': True,
	}

	onlines = list(db['online'].find({}, db_filter))
	other = False

	for online in onlines:
		if online['token'] == token:
			other = True

	## Emit to clients

	if not other:
		users_uniq = set()
		for online in onlines:
			users_uniq.add(online['token']) # !

		sio.emit('online_del', {
			'count': len(users_uniq),
			'users': [{'id': token}], # !
		}, namespace='/main')

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
