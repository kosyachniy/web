import string
import random
import hashlib
import time
import re

from func.mongodb import db
from api._error import ErrorSpecified, ErrorBusy, ErrorInvalid, \
					   ErrorWrong, ErrorUpload, ErrorAccess, ErrorCount
from api._func import check_params, get_preview, load_image, get_date, next_id


# # Token generation

# ALL_SYMBOLS = string.digits + string.ascii_letters
# generate = lambda length=32: ''.join(random.choice(ALL_SYMBOLS) for _ in range(length))

# Check name

def check_name(cont):
	# Недопустимое имя

	if not cont.isalpha():
		raise ErrorInvalid('name')

# Check surname

def check_surname(cont):
	# Недопустимая фамилия

	if not cont.isalpha():
		raise ErrorInvalid('surname')

# Check mail

def check_mail(cont, user):
	# Invalid mail

	if re.match('.+@.+\..+', cont) == None:
		raise ErrorInvalid('mail')

	# Mail is already registered

	users = db['users'].find_one({'mail': cont}, {'_id': True, 'id': True})
	if users and users['id'] != user['id']:
		raise ErrorBusy('mail')

# Check login

def check_login(cont, user):
	# Login is already registered

	users = db['users'].find_one({'login': cont}, {'_id': True, 'id': True})
	if users and users['id'] != user['id']:
		raise ErrorBusy('login')

	# Invalid login

	cond_length = not 3 <= len(cont) <= 20
	cond_symbols = len(re.findall('[^a-z0-9_]', cont))
	cond_letters = not len(re.findall('[a-z]', cont))

	if cond_length or cond_symbols or cond_letters:
		raise ErrorInvalid('login')

	# System reserved

	RESERVED = (
		'admin', 'administrator', 'test', 'tester', 'author', 'bot', 'robot',
		'root'
	)

	cond_id = cont[:2] == 'id'
	cond_reserv = cont in RESERVED

	if cond_id or cond_reserv:
		raise ErrorInvalid('login')

# Password

def check_password(cont):
	# Invalid password

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

# Account registration

def registrate(user, timestamp, login='', password='', mail='', name='', surname='', description='', avatar='', file='', social=[]):
	# ID

	user_id = next_id('users')

	# Login

	if login:
		login = login.lower()
		check_login(login, user)

	else:
		login = 'id{}'.format(user_id)

	# Mail

	if mail:
		mail = mail.lower()
		check_mail(mail, user)

	# Password

	if password:
		password = process_password(password)

	# Name

	if name:
		check_name(name)
		name = name.title()

	# Surname

	if surname:
		check_surname(surname)
		surname = surname.title()

	# Avatar

	if avatar:
		try:
			file_type = file.split('.')[-1]

		# Invalid file extension
		except:
			raise ErrorInvalid('file')

		try:
			load_image('users', avatar, user_id, file_type)

		# Error loading photo
		except:
			raise ErrorUpload('avatar')

	# Social networks
	# ! Добавить проверку социальных сетей

	#

	db['users'].insert_one({
		'id': user_id,
		'login': login,
		'password': password,
		'mail': mail,
		'name': name,
		'surname': surname,
		'description': description,
		# 'rating': 0,
		'admin': 3,
		'online': [],
		'social': social,
		'time': timestamp,
	})

	return user_id, login

#


# Sign up

def reg(this, **x):
	# Verification of parameters

	check_params(x, (
		('login', False, str),
		('password', False, str),
		('mail', False, str),
		('name', False, str),
		('surname', False, str),
		('social', False, list, dict),
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

	# Assigning the token to the user

	if not this.token:
		raise ErrorAccess('token')

	req = {
		'token': this.token,
		'id': user_id,
		'time': this.timestamp,
	}

	db['tokens'].insert_one(req)

	# Response

	res = {
		'id': user_id,
		'avatar': get_preview(user_id, 'users'),
		'admin': 3,
		# 'rating': 0,
		'login': login,
	}

	return res

# Social network

def social(this, **x):
	# Verification of parameters

	check_params(x, (
		('id', True, int), # ?
		('user', True, int),
		('hash', True, str),
		('data', True, dict),
	))

	# Sign in

	db_condition = {
		'social': {'$elemMatch': {'user': x['user'], 'hash': x['hash']}},
	}

	db_filter = {
		'_id': False,
		'id': True,
		'admin': True,
		# 'rating': True,
		'login': True,
	}

	res = db['users'].find_one(db_condition, db_filter)

	# Invalid password
	if not res:

		# Wrong hash

		db_condition = {
			'social': {'$elemMatch': {'user': x['user']}},
		}

		db_filter = {
			'_id': True,
		}

		res = db['users'].find_one(db_condition, db_filter)

		if res:
			raise ErrorWrong('hash')

		# Sign up
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
				# 'rating': True,
				'login': True,
			}

			res = db['users'].find_one({'id': user_id}, db_filter)

	# Assigning the token to the user

	if not this.token:
		raise ErrorInvalid('token')

	req = {
		'token': this.token,
		'id': res['id'],
		'time': this.timestamp,
	}

	db['tokens'].insert_one(req)

	# Response

	res = {
		'id': res['id'],
		'admin': res['admin'],
		# 'rating': res['rating'],
		'login': res['login'],
		'avatar': get_preview(res['id'], 'users'),
	}

	return res

# Log in

def auth(this, **x):
	# Verification of parameters

	check_params(x, (
		('login', True, str), # login / mail
		('password', True, str),
	))

	# Login

	x['login'] = x['login'].lower()

	db_condition = {'$or': [{
		'login': x['login'],
	}, {
		'mail': x['login'],
	}]}

	if not len(list(db['users'].find(db_condition, {'_id': True}))):
		raise ErrorWrong('login')

	# Password

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
		# 'rating': True,
		'login': True,
	}

	res = db['users'].find_one(db_condition, db_filter)

	## Wrong password
	if not res:
		raise ErrorWrong('password')

	# Assigning the token to the user

	if not this.token:
		raise ErrorInvalid('token')

	req = {
		'token': this.token,
		'id': res['id'],
		'time': this.timestamp,
	}

	db['tokens'].insert_one(req)

	# Response

	res = {
		'id': res['id'],
		'admin': res['admin'],
		# 'rating': res['rating'],
		'login': res['login'],
		'avatar': get_preview(res['id'], 'users'),
	}

	return res

# Log out

def exit(this, **x):
	# Not authorized
	if not this.token:
		raise ErrorAccess('token')

	# Check token
	res = db['tokens'].find_one({'token': this.token}, {'_id': True})

	# Wrong token
	if not res:
		raise ErrorWrong('token')

	# Remove token
	db['tokens'].remove(res['_id'])

# Edit personal information

def edit(this, **x):
	# Verification of parameters
	check_params(x, (
		('name', False, str),
		('surname', False, str),
		('login', False, str),
		('description', False, str),
		('mail', False, str),
		('avatar', False, str),
		('file', False, str),
		('social', False, list, dict),
	))

	# No access
	if this.user['admin'] < 3:
		raise ErrorAccess('token')

	# Name
	if 'name' in x:
		check_name(x['name'])
		this.user['name'] = x['name'].title()

	# Surname
	if 'surname' in x:
		check_surname(x['surname'])
		this.user['surname'] = x['surname'].title()

	# Login
	if 'login' in x:
		x['login'] = x['login'].lower()

		if this.user['login'] != x['login']:
			check_login(x['login'], this.user)
			this.user['login'] = x['login']

	# Mail
	if 'mail' in x:
		check_mail(x['mail'], this.user)

	# Password
	if 'password' in x:
		x['password'] = process_password(x['password'])

	# Change fields
	for i in ('description', 'mail', 'password', 'social'):
		if i in x:
			this.user[i] = x[i]

	# Save changes
	db['users'].save(this.user)

	# Avatar
	if 'avatar' in x:
		try:
			file_type = x['file'].split('.')[-1]

		# Invalid file extension
		except:
			raise ErrorInvalid('file')

		try:
			load_image('users', x['avatar'], this.user['id'], file_type)

		# Error loading photo
		except:
			raise ErrorUpload('avatar')

# # Recover password

# def recover(this, **x):
# 	# Verification of parameters

# 	check_params(x, (
# 		('login', True, str),
# 	))

# 	# Get user

# 	users = db['users'].find_one({'login': x['login']})

# 	if not users:
# 		raise ErrorWrong('login')

# 	password = ''.join(random.sample(ALL_SYMBOLS, 15))
# 	password_crypt = hashlib.md5(bytes(password, 'utf-8')).hexdigest()

# 	# Send

# 	# Update password

# 	users['password'] = password_crypt
# 	db['users'].save(users)