import time

from mongodb import db
from api._error import ErrorInvalid, ErrorAccess, ErrorWrong, ErrorUpload
from api._func import reimg, get_user, check_params, get_preview, next_id, load_image


# Создание / редактирование

def edit(this, **x):
	# Проверка параметров

	# Редактирование
	if 'id' in x:
		check_params(x, (
			('id', True, int),
			('name', False, str),
			('cont', False, str),
			('cover', False, str),
			('file', False, str),
			('category', False, int),
			('tags', False, list, str),
		))

	# Создание
	else:
		check_params(x, (
			('name', True, str),
			('cont', True, str),
			('cover', False, str),
			('file', False, str),
			('category', False, int),
			('tags', False, list, str),
		))

	# Формирование поста

	if 'id' in x:
		post = db['posts'].find_one({'id': x['id']})

		# Неправильный id
		if not post:
			raise ErrorWrong('id')

	else:
		post = {
			'id': next_id('posts'),
			'time': this.timestamp,
		}

	# Изменений полей

	for field in ('name', 'category', 'tags'):
		if field in x:
			post[field] = x[field]

	if 'cont' in x:
		post['cont'] = reimg(x['cont'])

	if 'cover' in x:
		try:
			file_type = x['file'].split('.')[-1]

		# Неправильное расширение
		except:
			raise ErrorInvalid('file')

		try:
			load_image('posts', x['cover'], post['id'], file_type)

		# Ошибка загрузки обложки
		except:
			raise ErrorUpload('cover')

	# Сохранение

	db['posts'].save(post)

	# Ответ

	res = {
		'id': post['id'],
	}

	return res

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