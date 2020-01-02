from app import app, sio
from flask import request # , session

import os
import time
import re

from mongodb import db


# Socket.IO

from threading import Lock
from flask_socketio import emit

thread = None
thread_lock = Lock()


# Онлайн пользователи

@sio.on('connect', namespace='/main')
def connect():
	global thread
	with thread_lock:
		if thread is None:
			thread = sio.start_background_task(target=background_thread)

	print('IN', request.sid)

@sio.on('online', namespace='/main')
def online(x):
	print('ON', request.sid)

	timestamp = time.time()

	# Онлайн пользователи

	online = {
		'sid': request.sid,
		'token': x['token'],
		'start': timestamp,
		'time': timestamp,
	}

	db['online'].insert_one(online)

	onlines = list(db['online'].find({}, {'_id': False, 'sid': True}))

	sio.emit('online_add', {
		'count': len(onlines),
		'users': onlines,
	}, namespace='/main')

@sio.on('disconnect', namespace='/main')
def disconnect():
	print('OUT', request.sid)

	# Онлайн пользователи

	online = db['online'].find_one({'sid': request.sid})
	if not online:
		return

	db['online'].remove(online['_id'])

	onlines = list(db['online'].find({}, {'_id': False, 'sid': True}))

	sio.emit('online_del', {
		'count': len(onlines),
		'users': onlines,
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
