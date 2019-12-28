import time

from mongodb import db
from api._error import ErrorInvalid, ErrorAccess
from api._func import reimg, get_user, check_params, get_preview


# Получение

def get(this, **x):
	# Проверка параметров

	check_params(x, (
		('id', False, (int, list, tuple), int),
		('count', False, int),
		('category', False, int),
		('language', False, (int, str)),
	))

	# Список постов

	db_condition = {}

	if 'id' in x:
		if type(x['id']) == int:
			db_condition['id'] = x['id']
		
		else:
			db_condition['id'] = {'$in': x['id']}

	# # Язык

	# if 'language' in x:
	# 	x['language'] = get_language(x['language'])
	# else:
	# 	x['language'] = this.language

	# Получение постов

	count = x['count'] if 'count' in x else None

	db_filter = {
		'_id': False,
		'id': True,
		'name': True,
		'cont': True,
	}

	posts = db['posts'].find(db_condition, db_filter)[:count]

	###

	res = {
		'posts': [{
			'id': post['id'],
			'name': post['name'],
			'cont': post['cont'],
			'cover': get_preview(post['id']),
			'tags': ['Программирование', 'Маркетинг'],
		} for post in posts]
	}

	return res

# Создание / редактирование

def edit(this, **x):
	post = db['posts'].find_one({'id': x['id']})

	post['cont'] = reimg(x['cont'])

	db['posts'].save(post)