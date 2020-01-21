import time

from func.mongodb import db
from api._error import ErrorInvalid, ErrorAccess
from api._func import reimg, get_user, check_params, next_id


# Добавить

def add(this, **x):
	# Проверка параметров

	check_params(x, (
		('name', True, str),
		('cont', True, str),
	))

	#

	query = {
		'id': next_id('feedback'),
		'name': x['name'],
		'cont': reimg(x['cont']),
		'user': this.user['id'],
		'time': this.timestamp,
		'success': 0,
	}

	db['feedback'].insert(query)

	# Ответ

	res = {
		'id': query['id'],
	}

	return res

# Получить

def get(this, **x):
	# Проверка параметров

	check_params(x, (
		('count', False, int),
	))

	# Нет доступа

	if this.user['admin'] < 4:
		raise ErrorAccess('token')

	#

	count = x['count'] if 'count' in x else None

	news = list(db['feedback'].find({}, {'_id': False}).sort('time', -1)[0:count])

	for i in range(len(news)):
		news[i]['user'] = get_user(news[i]['user'])

	# Ответ

	res = {
		'feedback': news,
	}

	return res

# Удалить

def delete(this, **x):
	# Проверка параметров

	check_params(x, (
		('id', True, int),
	))

	# Нет доступа

	if this.user['admin'] < 5:
		raise ErrorAccess('token')

	#

	feedback = db['feedback'].find_one({'id': x['id']}, {'_id': True})

	# Неправильный отзыв
	if not feedback:
		raise ErrorInvalid('feedback')

	db['feedback'].remove(feedback['_id'])