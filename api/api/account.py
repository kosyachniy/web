import string
import random
import hashlib
import time
import re

from mongodb import db
from api._error import ErrorSpecified, ErrorBusy, ErrorInvalid, \
					   ErrorWrong, ErrorUpload, ErrorAccess, ErrorCount
from api._func import check_params, get_preview, load_image, get_date, next_id


# Генерация токена

ALL_SYMBOLS = string.digits + string.ascii_letters
generate = lambda length=32: ''.join(random.choice(ALL_SYMBOLS) for _ in range(length))

# Проверить имя

def check_name(cont):
	# Недопустимое имя

	if not cont.isalpha():
		raise ErrorInvalid('name')

# Проверить фамилию

def check_surname(cont):
	# Недопустимая фамилия

	if not cont.isalpha():
		raise ErrorInvalid('surname')

# Проверить почту

def check_mail(cont, user):
	# Недопустимая почта

	if re.match('.+@.+\..+', cont) == None:
		raise ErrorInvalid('mail')

	# Почта уже зарегистрирована

	users = db['users'].find_one({'mail': cont}, {'_id': True, 'id': True})
	if users and users['id'] != user['id']:
		raise ErrorBusy('mail')

# Проверить логин

def check_login(cont, user):
	# Логин уже зарегистрирован

	users = db['users'].find_one({'login': cont}, {'_id': True, 'id': True})
	if users and users['id'] != user['id']:
		raise ErrorBusy('login')

	# Недопустимый логин

	cond_length = not 3 <= len(cont) <= 20
	cond_symbols = len(re.findall('[^a-z0-9_]', cont))
	cond_letters = not len(re.findall('[a-z]', cont))

	if cond_length or cond_symbols or cond_letters:
		raise ErrorInvalid('login')

	# Системно зарезервировано

	RESERVED = (
		'admin', 'administrator', 'test', 'tester', 'author', 'bot', 'robot', 
		'root'
	)

	cond_id = cont[:2] == 'id'
	cond_reserv = cont in RESERVED

	if cond_id or cond_reserv:
		raise ErrorInvalid('login')

# Пароль

def check_password(cont):
	# Недопустимый пароль

	cond_length = not 6 <= len(cont) <= 40
	pass_rule = '[^a-zA-z0-9!@#$%^&*()\-+=;:,./?\|`~\[\]\{\}]'
	cond_symbols = len(re.findall(pass_rule, cont))
	cond_letters = not len(re.findall('[a-zA-Z]', cont))
	cond_digits = not len(re.findall('[0-9]', cont))

	if cond_length or cond_symbols or cond_letters or cond_digits:
		raise ErrorInvalid('password')

def process_password(cont):
	check_password(cont)

	return hashlib.md5(bytes(cont, 'utf-8')).hexdigest()

# Регистрация аккаунта

def registrate(user, timestamp, login='', password='', mail='', name='', surname='', description='', avatar='', file='', social=[]):
	# ID

	user_id = next_id('users')

	# Логин

	if login:
		login = login.lower()
		check_login(login, user)

	else:
		login = 'id{}'.format(user_id)

	# Почта

	if mail:
		mail = mail.lower()
		check_mail(mail, user)

	# Пароль

	if password:
		password = process_password(password)

	# Имя

	if name:
		check_name(name)
		name = name.title()

	# Фамилия

	if surname:
		check_surname(surname)
		surname = surname.title()

	# Аватарка

	if avatar:
		try:
			file_type = file.split('.')[-1]

		# Неправильное расширение
		except:
			raise ErrorInvalid('file')

		try:
			load_image('users', avatar, user_id, file_type)

		# Ошибка загрузки фотографии
		except:
			raise ErrorUpload('avatar')

	# Социальные сети
	# ! Добавить проверку социальных сетей

	#

	db['users'].insert({
		'id': user_id,
		'login': login,
		'password': password,
		'mail': mail,
		'name': name,
		'surname': surname,
		'description': description,
		'rating': 0,
		'admin': 3,
		'ladders': [],
		'steps': [],
		'public': '',
		'online': [],
		'social': social,
		'time': timestamp,
	})

	return user_id, login

#


# Регистрация

def reg(this, **x):
	# Проверка параметров

	check_params(x, (
		('login', False, str),
		('password', False, str),
		('mail', False, str),
		('name', False, str),
		('surname', False, str),
		('social', False, (list, tuple), dict),
		('avatar', False, str),
		('file', False, str),
	))

	user_id, login = registrate(
		this.user,
		this.timestamp,
		login=x['login'] if 'login' in x else '',
		password=x['password'] if 'password' in x else '',
		mail=x['mail'] if 'mail' in x else '',
		name=x['name'] if 'name' in x else '',
		surname=x['surname'] if 'surname' in x else '',
		avatar=x['avatar'] if 'avatar' in x else '',
		file=x['file'] if 'file' in x else '',
		social=x['social'] if 'social' in x else [],
	)

	#

	token = generate()

	req = {
		'token': token,
		'id': user_id,
		'time': this.timestamp,
	}
	db['tokens'].insert(req)

	res = {
		'id': user_id,
		'token': token,
		'avatar': get_preview('users', user_id),
		'admin': 3,
		'rating': 0,
		'login': login,
	}

	return res

# Авторизация

def social(this, **x):
	# Проверка параметров

	check_params(x, (
		('id', True, int), # ?
		('user', True, int),
		('hash', True, str),
		('data', True, dict),
	))

	# Авторизация

	db_condition = {
		'social': {'$elemMatch': {'user': x['user'], 'hash': x['hash']}},
	}

	db_filter = {
		'_id': False,
		'id': True,
		'admin': True,
		'rating': True,
		'login': True,
	}

	res = db['users'].find_one(db_condition, db_filter)

	# Неправильный пароль
	if not res:

		# Регистрация

		db_condition = {
			'social': {'$elemMatch': {'user': x['user']}},
		}

		db_filter = {
			'_id': True,
		}

		res = db['users'].find_one(db_condition, db_filter)

		if res:
			raise ErrorWrong('hash')

		# Регистрация
		else:
			user_id, _ = registrate(
				this.user,
				this.timestamp,
				social=[{
					'id': x['id'],
					'user': x['user'],
					'hash': x['hash'],
					'data': x['data'],
				}],
			)

			#

			db_filter = {
				'_id': False,
				'id': True,
				'admin': True,
				'rating': True,
				'login': True,
			}

			res = db['users'].find_one({'id': user_id}, db_filter)

		#

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
		'rating': res['rating'],
		'login': res['login'],
		'avatar': get_preview('users', res['id']),
	}

	return res

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

	password = hashlib.md5(bytes(x['password'], 'utf-8')).hexdigest()

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
		'rating': res['rating'],
		'login': res['login'],
		'avatar': get_preview('users', res['id']),
	}

	return res

# Закрытие сессии

def exit(this, **x):
	# Не авторизован

	if not this.token:
		raise ErrorAccess('token')

	#

	res = db['tokens'].find_one({'token': this.token}, {'_id': True})

	# Неправильный токен

	if not res:
		raise ErrorWrong('token')

	#

	db['tokens'].remove(res['_id'])

# Изменение личной информации

def edit(this, **x):
	# Проверка параметров

	check_params(x, (
		('name', False, str),
		('surname', False, str),
		('login', False, str),
		('description', False, str),
		('mail', False, str),
		('avatar', False, str),
		('file', False, str),
		('templates', False, list, dict),
		('social', False, (list, tuple), dict),
	))

	# Нет доступа

	if this.user['admin'] < 3:
		raise ErrorAccess('token')

	# Имя

	if 'name' in x:
		check_name(x['name'])
		this.user['name'] = x['name'].title()

	# Фамилия

	if 'surname' in x:
		check_surname(x['surname'])
		this.user['surname'] = x['surname'].title()

	# Логин

	if 'login' in x:
		x['login'] = x['login'].lower()

		if this.user['login'] != x['login']:
			check_login(x['login'], this.user)
			this.user['login'] = x['login']

	# Описание, почта, пароль, шаблоны

	if 'mail' in x:
		check_mail(x['mail'], this.user)

	# Пароль

	if 'password' in x:
		x['password'] = process_password(x['password'])

	for i in ('description', 'mail', 'password', 'templates', 'social'):
		if i in x:
			this.user[i] = x[i]

	#

	db['users'].save(this.user)

	# Аватарка

	if 'avatar' in x:
		try:
			file_type = x['file'].split('.')[-1]

		# Неправильное расширение
		except:
			raise ErrorInvalid('file')

		try:
			load_image('users', x['avatar'], this.user['id'], file_type)

		# Ошибка загрузки фотографии
		except:
			raise ErrorUpload('avatar')

	#

# # Восстановить пароль

# def recover(this, **x):
# 	# Проверка параметров

# 	check_params(x, (
# 		('login', True, str),
# 	))

# 	#

# 	users = db['users'].find_one({'login': x['login']})

# 	if not users:
# 		raise ErrorWrong('login')

# 	password = ''.join(random.sample(ALL_SYMBOLS, 15))
# 	password_crypt = hashlib.md5(bytes(password, 'utf-8')).hexdigest()

# 	# Отправить



# 	# Обновить пароль

# 	users['password'] = password_crypt
# 	db['users'].save(users)