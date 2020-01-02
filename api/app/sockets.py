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


# Reset online users
db['online'].remove()


# Online users

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

	# Online users
	## Emit all users to this user

	onlines = list(db['online'].find({}, {'_id': False, 'id': True}))

	if len(onlines):
		sio.emit('online_add', {
			'count': len(onlines),
			'users': onlines,
		}, room=request.sid, namespace='/main')

	## Add to DB

	online = {
		'id': request.sid, # !
		'sid': request.sid,
		'token': x['token'],
		'start': timestamp,
		'time': timestamp,
	}

	db['online'].insert_one(online)

	## Emit this user to all users

	sio.emit('online_add', {
		'count': len(onlines)+1,
		'users': [{'id': request.sid}], # !
	}, namespace='/main')

@sio.on('disconnect', namespace='/main')
def disconnect():
	print('OUT', request.sid)

	# Online users
	## Remove from DB

	online = db['online'].find_one({'sid': request.sid})
	if not online:
		return

	db['online'].remove(online['_id'])

	## Emit to clients

	onlines = list(db['online'].find({}, {'_id': False, 'id': True}))

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
