import time

from mongodb import db
from api._error import ErrorInvalid, ErrorAccess
from api._func import reimg, get_user, check_params


def add(this, **x):
	# Проверка параметров

	check_params(x, (
		('token', False, str),
		('name', True, str),
		('cont', True, str),
	))

	#

	try:
		id = db['feedback'].find({}, {'_id': False, 'id': True}).sort('id', -1)[0]['id'] + 1
	except:
		id = 1

	query = {
		'id': id,
		'name': x['name'],
		'cont': reimg(x['cont']),
		'user': this.user['id'],
		'time': this.timestamp,
		'success': 0,
	}

	db['feedback'].insert(query)

	res = {
		'id': id,
	}

	return res

#

def get(this, **x):
	# Проверка параметров

	check_params(x, (
		('token', False, str),
		('count', False, int),
	))

	# Нет прав на просмотр отзывов
	if this.user['admin'] < 4:
		raise ErrorAccess('get')
		# return dumps({'error': 6, 'message': ERROR[15]})

	count = x['count'] if 'count' in x else None

	news = list(db['feedback'].find({}, {'_id': False}).sort('time', -1)[0:count])

	for i in range(len(news)):
		news[i]['user'] = get_user(news[i]['user'])

	res = {
		'feedback': news,
	}

	return res

#

def delete(this, **x):
	# Проверка параметров

	check_params(x, (
		('token', True, str),
		('id', True, int),
	))

	#

	feedback = db['feedback'].find_one({'id': x['id']}, {'_id': True})

	# Неправильный отзыв
	if not feedback:
		raise ErrorInvalid('feedback')
		# return dumps({'error': 6, 'message': ERROR[33]})

	# Нет прав на удаление отзыва
	if this.user['admin'] < 5:
		raise ErrorAccess('delete')
		# return dumps({'error': 7, 'message': ERROR[15]})

	db['feedback'].remove(feedback['_id'])