import string
import random
from hashlib import md5
import time
import re

from mongodb import db
from api._error import ErrorSpecified, ErrorBusy, ErrorInvalid, ErrorWrong, ErrorUpload
from api._func import check_params, get_preview


# Генерация токена

ALL_SYMBOLS = string.digits + string.ascii_letters
generate = lambda length=32: ''.join(random.choice(ALL_SYMBOLS) for _ in range(length))


# Регистрация

def reg(this, **x):
	# Проверка параметров

	check_params(x, (
		('login', True, str),
		('password', True, str),
		('mail', True, str),
		('name', False, str),
		('surname', False, str),
	))

	#

	x['login'] = x['login'].lower()

	# Логин уже зарегистрирован

	if len(list(db['users'].find({'login': x['login']}, {'_id': True}))):
		raise ErrorBusy('login')
		# return dumps({'error': 6, 'message': ERROR[4]})

	# Недопустимый логин

	cond_length = not 3 <= len(x['login']) <= 20
	cond_symbols = len(re.findall('[^a-z0-9]', x['login']))
	cond_letters = not len(re.findall('[a-z]', x['login']))

	if cond_length or cond_symbols or cond_letters:
		raise ErrorInvalid('login')
		# return dumps({'error': 7, 'message': ERROR[5]})

	# Почта уже зарегистрирована

	if len(list(db['users'].find({'mail': x['mail']}, {'_id': True}))):
		raise ErrorBusy('mail')
		# return dumps({'error': 8, 'message': ERROR[6]})

	# Недопустимый пароль

	cond_length = not 6 <= len(x['password']) <= 40
	pass_rule = '[^a-zA-z0-9!@#$%^&*()-_+=;:,./?\|`~\[\]{}]'
	cond_symbols = len(re.findall(pass_rule, x['password']))
	cond_letters = not len(re.findall('[a-zA-Z]', x['password']))
	cond_digits = not len(re.findall('[0-9]', x['password']))

	if cond_length or cond_symbols or cond_letters or cond_digits:
		raise ErrorInvalid('password')
		# return dumps({'error': 9, 'message': ERROR[7]})

	# Недопустимая почта

	if re.match('.+@.+\..+', x['mail']) == None:
		raise ErrorInvalid('mail')
		# return dumps({'error': 10, 'message': ERROR[8]})

	# Недопустимое имя

	if 'name' in x and not x['name'].isalpha():
		raise ErrorInvalid('name')
		# return dumps({'error': 11, 'message': ERROR[9]})

	# Недопустимая фамилия

	if 'surname' in x and not x['surname'].isalpha():
		raise ErrorInvalid('surname')
		# return dumps({'error': 12, 'message': ERROR[10]})

	#

	try:
		db_filter = {'id': True, '_id': False}
		id = db['users'].find({}, db_filter).sort('id', -1)[0]['id'] + 1
	except:
		id = 1

	db['users'].insert({
		'id': id,
		'login': x['login'],
		'password': md5(bytes(x['password'], 'utf-8')).hexdigest(),
		'mail': x['mail'].lower(),
		'name': x['name'].title() if 'name' in x else None,
		'surname': x['surname'].title() if 'surname' in x else None,
		'description': '',
		'rating': 0,
		'admin': 3,
		'ladders': [],
		'steps': [],
		'balance': 1000, #
		'public': '', #
		'templates': [{
			'name': 'Задание по математике. Базовый шаблон',
			'cont': '<h3>Здесь формулируется задание:</h3><p>&nbsp;</p><p><img alt="\\large Пример" src="http://latex.codecogs.com/gif.latex?%5Cdpi%7B200%7D%20%5Clarge%20%u041F%u0440%u0438%u043C%u0435%u0440" /><img alt="\\large \\frac{Formula}{\\sqrt{(xy)^3}} = \\ ?" src="http://latex.codecogs.com/gif.latex?%5Cdpi%7B200%7D%20%5Clarge%20%5Cfrac%7BFormula%7D%7B%5Csqrt%7B%28xy%29%5E3%7D%7D%20%3D%20%5C%20%3F" /></p><p>&nbsp;</p><hr /><h6>* Здесь находятся комментарии по поводу ввода ответа, например:</h6><h6>* Если ответов несколько, введите их через точку с запятой.</h6><h6>* В десятичных доробях целая и дробная части отделяются друг от друга запятой</h6><h6>* Запишите в ответ интервал с пробелами после точек с запятой,</h6><h6>* &infin; - знак бесконечности (можно скопировать, если нужен&nbsp;в ответе).</h6><h6>* ⋃ - знак объединения (в виде заглавной u).</h6><h6>* Пример ответа:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;(-&infin;: 0]U[7; +&infin;)</h6>',
		}, {
			'name': 'Теория по математике. Базовый шаблон',
			'cont': '<p>Допустим, задание по математике такое:</p><p><img src="http://tensy.org/static/load/steps/18-5-1.png" /></p><p>Тогда соответствующая теория может выглядеть следующим образом:</p><p>&nbsp;</p><p>1) Находим ограничения на область допустимых значений&nbsp;&nbsp;<img alt="x" src="http://latex.codecogs.com/gif.latex?%5Cdpi%7B120%7D%20x" />;</p><p>2) Представляем правую часть в виде логарифма с основанием таким же, как&nbsp; в выражении слева;</p><p>3) &quot;Избавляемся&quot; от логарифмов. При этом обращаем внимание на основание. Основание&nbsp;&nbsp;<img alt="&gt;1" src="http://latex.codecogs.com/gif.latex?%3E1" />, следовательно знак неравенсва не изменяется;</p><p>4) Решаем получившееся рациональное неравенство методом интервалов.</p>',
		}],
		'online': [],
	})

	token = generate()

	req = {
		'token': token,
		'id': id,
		'time': this.timestamp,
	}
	db['tokens'].insert(req)

	res = {
		'id': id,
		'token': token,
		'avatar': get_preview('users', id),
	}

	return res

# Авторизация

def auth(this, **x):
	# Проверка параметров

	check_params(x, (
		('login', True, str), # Логин или почта
		('password', True, str),
	))

	#

	x['login'] = x['login'].lower()

	# Логин

	db_condition = {'$or': [{
		'login': x['login'],
	}, {
		'mail': x['login'],
	}]}

	if not len(list(db['users'].find(db_condition, {'_id': True}))):
		raise ErrorWrong('login')
		# return dumps({'error': 6, 'message': ERROR[11]})
	
	# Пароль

	password = md5(bytes(x['password'], 'utf-8')).hexdigest()

	db_condition = {
		'$or': [{
			'login': x['login'],
		}, {
			'mail': x['login'],
		}],
		'password': password,
	}

	db_filter = {
		'_id': False,
		'id': True,
		'admin': True,
		'balance': True,
		'rating': True,
		'login': True,
	}

	res = db['users'].find_one(db_condition, db_filter)

	# Неправильный пароль
	if not res:
		raise ErrorWrong('password')
		# return dumps({'error': 7, 'message': ERROR[12]})

	token = generate()

	req = {
		'token': token,
		'id': res['id'],
		'time': this.timestamp,
	}
	db['tokens'].insert(req)

	res = {
		'id': res['id'],
		'token': token,
		'admin': res['admin'],
		'balance': res['balance'],
		'rating': res['rating'],
		'login': res['login'],
		'avatar': get_preview('users', res['id']),
	}

	return res

# Закрытие сессии

def exit(this, **x):
	# Проверка параметров

	check_params(x, (
		('token', True, str),
	))

	#

	res = db['tokens'].find_one({'token': x['token']}, {'_id': True})

	# Неправильный токен

	if not res:
		raise ErrorWrong('token')

	#

	db['tokens'].remove(res['_id'])

# Изменение личной информации

def edit(this, **x):
	# Проверка параметров

	check_params(x, (
		('token', True, str),
		('name', False, str),
		('surname', False, str),
		('description', False, str),
		('photo', False, str),
		('templates', False, list, dict),
	))

	# Имя

	if 'name' in x:
		# Недопустимое имя
		if not x['name'].isalpha():
			raise ErrorInvalid('name')
			# return dumps({'error': 6, 'message': ERROR[9]})

		this.user['name'] = x['name'].title()

	# Фамилия

	if 'surname' in x:
		# Недопустимая фамилия
		if not x['surname'].isalpha():
			raise ErrorInvalid('surname')
			# return dumps({'error': 7, 'message': ERROR[10]})

		this.user['surname'] = x['surname'].title()

	# Описание, почта, пароль, шаблоны

	for i in ('description', 'mail', 'password', 'templates'):
		if i in x:
			this.user[i] = x[i]

	#

	db['users'].save(this.user)

	# Аватарка

	if 'photo' in x:
		try:
			load_image('app/static/load/users', x['photo'], this.user['id'])

		# Ошибка загрузки фотографии
		except:
			raise ErrorUpload('photo')
			# return dumps({'error': 8, 'message': ERROR[13]})

	#

# # Восстановить пароль

# def recover(this, **x):
# 	# Проверка параметров

# 	check_params(x, (
# 		('token', False, str),
# 		('login', True, str),
# 	))

# 	#

# 	users = db['users'].find_one({'login': x['login']})

# 	if not users:
# 		raise ErrorWrong('login')

# 	password = ''.join(random.sample(ALL_SYMBOLS, 15))
# 	password_crypt = md5(bytes(password, 'utf-8')).hexdigest()

# 	# Отправить



# 	# Обновить пароль

# 	users['password'] = password_crypt
# 	db['users'].save(users)