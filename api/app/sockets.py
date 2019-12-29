from app import app, sio
from flask import request # , session

import os
import time
import re


# Socket.IO

from threading import Lock
from flask_socketio import emit

thread = None
thread_lock = Lock()


# Онлайн пользователи

@sio.on('connect', namespace='/main')
def online():
	# global thread
	# with thread_lock:
	# 	if thread is None:
	# 		thread = sio.start_background_task(target=background_thread)

	print('IN', request.sid, rooms())

@sio.on('disconnect', namespace='/main')
def online():
	print('OUT', rooms())

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

		time.sleep(1)
