import string
import random
import hashlib
import re
import requests
import urllib
import json
import base64

from sets import CLIENT, IMAGE
from func.mongodb import db
from func.smsc import SMSC
from api._error import ErrorSpecified, ErrorBusy, ErrorInvalid, \
					   ErrorWrong, ErrorUpload, ErrorAccess, ErrorCount, \
					   ErrorRepeat
from api._func import check_params, load_image, get_date, next_id, \
					  online_emit_add, other_sessions, online_user_update, \
					  online_emit_del


with open('keys.json', 'r') as file:
	keys = json.loads(file.read())
	VK = keys['vk']
	GOOGLE = keys['google']


# # Token generation

# ALL_SYMBOLS = string.digits + string.ascii_letters
# generate = lambda length=32: ''.join(random.choice(ALL_SYMBOLS) for _ in range(length))

# Check name

def check_name(cont):
	# Invalid name

	if not cont.isalpha():
		raise ErrorInvalid('name')

# Check surname

def check_surname(cont):
	# Invalid surname

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
		'admin', 'administrator', 'author', 'test', 'tester', 'bot', 'robot',
		'root', 'info', 'support', 'manager', 'client', 'dev', 'account',
		'user', 'users', 'profile', 'login', 'password', 'code', 'mail',
		'phone', 'google', 'facebook', 'administration',
	)

	cond_id = cont[:2] == 'id'
	cond_reserv = cont in RESERVED

	if cond_id or cond_reserv:
		raise ErrorInvalid('login')

# Password

def check_password(cont):
	# Invalid password

	cond_length = not 6 <= len(cont) <= 40
	pass_rule = '[^a-zA-Z0-9!@#$%&*--+=,./?|~]' # ! --
	cond_symbols = len(re.findall(pass_rule, cont))
	cond_letters = not len(re.findall('[a-zA-Z]', cont))
	cond_digits = not len(re.findall('[0-9]', cont))

	if cond_length or cond_symbols or cond_letters or cond_digits:
		raise ErrorInvalid('password')

def process_password(cont):
	check_password(cont)

	return hashlib.md5(bytes(cont, 'utf-8')).hexdigest()

# Phone number

def process_phone(cont):
	if not len(cont):
		raise ErrorInvalid('phone')

	if cont[0] == '8':
		cont = '7' + cont[1:]

	cont = re.sub('[^0-9]', '', cont)

	if len(cont) != 11:
		raise ErrorInvalid('phone')

	return int(cont)

# Account registration

def registrate(user, timestamp, login='', password='', mail='', name='', surname='', description='', avatar='', file='', social=[], phone=None):
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

	link = 'users/0.png'

	if avatar:
		try:
			file_type = file.split('.')[-1]

		# Invalid file extension
		except:
			raise ErrorInvalid('file')

		try:
			link = load_image(avatar, file_type)

		# Error loading photo
		except:
			raise ErrorUpload('avatar')

	# Social networks
	# ! Добавить проверку социальных сетей

	# # Referal link

	# ALL_SYMBOLS = string.ascii_lowercase + string.digits
	# generate = lambda length=8: ''.join(random.choice(ALL_SYMBOLS) for _ in range(length))
	# referal_code = generate()

	#

	req = {
		'id': user_id,
		'login': login,
		'password': password,
		'name': name,
		'surname': surname,
		'avatar': link,
		'admin': 3,
		'mail': mail,
		# 'balance': 0,
		# 'rating': 0,
		'description': description,
		'time': timestamp,
		'online': [],
		'social': social,
		# 'referal_code': referal_code,
		'referal_parent': 0,
	}

	if phone:
		req['phone'] = phone

	db['users'].insert_one(req)

	# Response

	return req

# Update online users

def online_update(sio, user, token):
	# Online users
	## Already online

	if other_sessions(user['id']):
		return

	## Update DB

	for i in db['online'].find({'token': token}):
		i['id'] = user['id']
		i['login'] = user['login']
		i['name'] = user['name']
		i['surname'] = user['surname']
		i['avatar'] = IMAGE['link_opt'] + user['avatar']
		i['admin'] = user['admin']

		db['online'].save(i)

	## Emit this user to all users

	online_emit_add(sio, user)

	# ! Сокет на обновление сессий в браузере

#

# Sign up
# ! Сокет на авторизацию на всех вкладках токена
# ! Перезапись информации этого токена уже в онлайне

def reg(this, **x):
	# Checking parameters

	check_params(x, (
		('login', False, str),
		('password', False, str),
		('name', False, str),
		('surname', False, str),
		('avatar', False, str),
		('file', False, str),
		('mail', False, str),
		('social', False, list, dict),
	))

	user = registrate(
		this.user,
		this.timestamp,
		login=x['login'] if 'login' in x else '',
		password=x['password'] if 'password' in x else '',
		name=x['name'] if 'name' in x else '',
		surname=x['surname'] if 'surname' in x else '',
		avatar=x['avatar'] if 'avatar' in x else '',
		file=x['file'] if 'file' in x else '',
		mail=x['mail'] if 'mail' in x else '',
		social=x['social'] if 'social' in x else [],
	)

	# Assignment of the token to the user

	if not this.token:
		raise ErrorAccess('token')

	req = {
		'token': this.token,
		'id': user['id'],
		'time': this.timestamp,
	}

	db['tokens'].insert_one(req)

	# Update online users

	online_update(this.socketio, user, this.token)

	# Response

	res = {
		'id': user['id'],
		'login': user['login'],
		'name': user['name'],
		'surname': user['surname'],
		'avatar': IMAGE['link_opt'] + user['avatar'],
		'admin': 3,
		'mail': user['mail'],
		# 'balance': 0,
		# 'rating': 0,
	}

	return res

# By social network

def social(this, **x):
	# Checking parameters

	check_params(x, (
		('id', True, int), # 1-ВКонтакте, 2-Telegram, 3-Google, 4-FaceBook, 5-Apple, 6-Twitter, 7-GitHub
		('code', True, str),
	))

	#

	user_id = 0
	new = False
	mail = ''

	# ВКонтакте
	if x['id'] == 1:
		link = 'https://oauth.vk.com/access_token?client_id={}&client_secret={}&redirect_uri={}callback&code={}'
		response = json.loads(requests.get(link.format(VK['client_id'], VK['client_secret'], CLIENT['link'], x['code'])).text)

		if 'user_id' in response:
			user_id = response['user_id']
		else:
			raise ErrorAccess('code')

		if 'email' in response:
			mail = response['email']

	# Google
	elif x['id'] == 3:
		link = 'https://accounts.google.com/o/oauth2/token'
		cont = {
			'client_id': GOOGLE['client_id'],
			'client_secret': GOOGLE['client_secret'],
			'redirect_uri': '{}callback'.format(CLIENT['link']),
			'grant_type': 'authorization_code',
			'code': urllib.parse.unquote(x['code']),
		}
		response = json.loads(requests.post(link, json=cont).text)

		if 'access_token' not in response:
			raise ErrorAccess('code')

		link = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'
		response = json.loads(requests.get(link.format(response['access_token'])).text)

		if 'id' in response:
			user_id = response['id']
		else:
			raise ErrorAccess('code')

	# Wrong ID

	if not user_id:
		raise ErrorWrong('id')

	# Sign in

	db_condition = {
		'social': {'$elemMatch': {'id': x['id'], 'user': user_id}},
	}

	db_filter = {
		'_id': False,
		'id': True,
		'login': True,
		'name': True,
		'surname': True,
		'avatar': True,
		'admin': True,
		'mail': True,
		# 'rating': True,
		# 'balance': True,
	}

	res = db['users'].find_one(db_condition, db_filter)

	# Wrong password
	if not res:
		# Check keys

		name = ''
		surname = ''
		login = ''
		avatar = ''

		if x['id'] == 1:
			if 'access_token' in response:
				token = response['access_token']
			else:
				raise ErrorAccess('code')

			# link = 'https://api.vk.com/method/account.getProfileInfo?access_token={}&v=5.103'
			link = 'https://api.vk.com/method/users.get?user_ids={}&fields=photo_max_orig,nickname&access_token={}&v=5.103'

			try:
				response = json.loads(requests.get(link.format(user_id, token)).text)['response'][0]
			except:
				raise ErrorAccess('vk')

			try:
				name = response['first_name']
				check_name(name)
			except:
				name = ''

			try:
				surname = response['last_name']
				check_surname(surname)
			except:
				surname = ''

			try:
				login = response['nickname']
				check_login(login, this.user)
			except:
				login = ''

			try:
				avatar = str(base64.b64encode(requests.get(response['photo_max_orig']).content))[2:-1]
			except:
				avatar = ''

			try:
				if mail:
					check_mail(mail, this.user)
			except:
				mail = ''

		elif x['id'] == 3:
			# link = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(x['data']['access_token'])
			# res_google = json.loads(requests.get(link).text)

			try:
				name = response['given_name']
				check_name(name)
			except:
				name = ''

			try:
				surname = response['family_name']
				check_surname(surname)
			except:
				surname = ''

			try:
				mail = response['email']
				check_mail(mail, this.user)
			except:
				mail = ''

			try:
				if response['picture']:
					avatar = str(base64.b64encode(requests.get(response['picture']).content))[2:-1]
			except:
				pass

		# Sign up

		db_condition = {
			'social': {'$elemMatch': {'user': user_id}},
		}

		db_filter = {
			'_id': True,
		}

		res = db['users'].find_one(db_condition, db_filter)

		if res:
			raise ErrorWrong('hash')

		# Sign up
		else:
			new = True

			res = registrate(
				this.user,
				this.timestamp,
				social=[{
					'id': x['id'],
					'user': user_id,
				}],
				name = name,
				surname = surname,
				avatar = avatar,
				mail = mail,
			)

			#

			db_filter = {
				'_id': False,
				'id': True,
				'admin': True,
				# 'balance': True,
				# 'rating': True,
				'login': True,
				'name': True,
				'surname': True,
				'mail': True,
			}

			res = db['users'].find_one({'id': res['id']}, db_filter)

	# Assignment of the token to the user

	if not this.token:
		raise ErrorInvalid('token')

	req = {
		'token': this.token,
		'id': res['id'],
		'time': this.timestamp,
	}
	db['tokens'].insert_one(req)

	# Update online users

	online_update(this.socketio, res, this.token)

	# Response

	res = {
		'id': res['id'],
		'login': res['login'],
		'name': res['name'],
		'surname': res['surname'],
		'avatar': IMAGE['link_opt'] + res['avatar'],
		'admin': res['admin'],
		'mail': res['mail'],
		# 'balance': res['balance'],
		# 'rating': res['rating'],
		'new': new,
	}

	return res

# By phone

def phone_send(this, **x):
	# Checking parameters

	check_params(x, (
		('phone', True, str),
		('promo', False, str),
	))

	# Process a phone number

	phone = process_phone(x['phone'])

	# Already sent

	code = db['codes'].find_one({'phone': phone}, {'_id': True})

	if code:
		raise ErrorRepeat('send')

	# Code generation

	ALL_SYMBOLS = string.digits
	generate = lambda length=4: ''.join(random.choice(ALL_SYMBOLS) for _ in range(length))
	code = generate()

	#

	req = {
		'phone': phone,
		'code': code,
		'token': this.token,
		'time': this.timestamp,
	}

	if 'promo' in x:
		req['promo'] = x['promo']

	db['codes'].insert_one(req)

	#

	sms = SMSC()
	res = sms.send_sms(str(phone), 'Hi!\n{} — This is your login code.'.format(code))
	print(phone, res)

	# Response

	res = {
		'phone': phone,
		'status': int(float(res[-1])) > 0,
	}

	return res

def phone_check(this, **x):
	# Checking parameters

	check_params(x, (
		('phone', False, str),
		('code', False, (int, str)),
		('promo', False, str),
	))

	#

	if not this.token:
		raise ErrorInvalid('token')

	#

	if 'code' in x and not x['code']:
		del x['code']

	if 'phone' in x:
		x['phone'] = process_phone(x['phone'])

	#

	if 'code' in x:
		# Code preparation

		x['code'] = str(x['code'])

		# Verification of code

		db_condition = {
			'code': x['code'],
		}

		if 'phone' in x:
			db_condition['phone'] = x['phone']
		else:
			db_condition['token'] = this.token

		db_filter = {
			'_id': False,
			'phone': True,
		}

		code = db['codes'].find_one(db_condition, db_filter)

		if code:
			# ! Входить по старым кодам
			pass
			# db['codes'].remove(code)

		else:
			raise ErrorWrong('code')

	else:
		code = {
			'phone': x['phone'],
		}

		if 'promo' in x:
			code['promo'] = x['promo']

	#

	user = db['users'].find_one({'phone': code['phone']})

	#

	new = False

	if not user:
		res = registrate(
			this.user,
			this.timestamp,
			phone=code['phone'],
		)

		new = True

		#

		user = db['users'].find_one({'id': res['id']})

	if 'promo' in code:
		# Referal code

		if code['promo'].lower()[:5] == 'tensy':
			referal_parent = int(re.sub('\D', '', code['promo']))

			if user['id'] != referal_parent:
				user['referal_parent'] = referal_parent
				db['users'].save(user)

		else:
			# Bonus code

			promo = db['promos'].find_one({'promo': code['promo'].upper()})

			if not promo:
				promo = db['promos'].find_one({'promo': code['promo'].lower()})

				if promo:
					# Нет доступа

					if user['admin'] >= promo['admin']:
						# Повтор

						if promo['repeat'] or user['id'] not in promo['users']:
							# Выполнение скрипта

							user['balance'] += promo['balance']
							db['users'].save(user)

							# Сохранение результатов в промокоде

							promo['users'].append(user['id'])
							db['promos'].save(promo)

	# Присвоение токена пользователю

	req = {
		'token': this.token,
		'id': user['id'],
		'time': this.timestamp,
	}
	db['tokens'].insert_one(req)

	# Update online users

	online_update(this.socketio, user, this.token)

	# Response

	res = {
		'id': user['id'],
		'login': user['login'],
		'name': user['name'],
		'surname': user['surname'],
		'avatar': IMAGE['link_opt'] + user['avatar'],
		'admin': user['admin'],
		'mail': user['mail'],
		# 'balance': user['balance'],
		# 'rating': user['rating'],
		'new': new,
	}

	return res

# Log in
# ! Сокет на авторизацию на всех вкладках токена
# ! Перезапись информации этого токена уже в онлайне

def auth(this, **x):
	# Checking parameters

	check_params(x, (
		('login', True, str), # login / mail
		('password', True, str),
	))

	#

	x['login'] = x['login'].lower()

	# if 'password' in x and not x['password']:
	# 	del x['password']

	# Login

	x['login'] = x['login'].lower()

	db_condition = {'$or': [{
		'login': x['login'],
	}, {
		'mail': x['login'],
	}]}

	new = False

	if not db['users'].find_one(db_condition, {'_id': True}):
		# raise ErrorWrong('login')

		registrate(
			this.user,
			this.timestamp,
			mail=x['login'],
			password=x['password'],
		)

		new = True

	#

	db_condition = {
		'$or': [{
			'login': x['login'],
		}, {
			'mail': x['login'],
		}],
	}

	# Пароль
	# if 'password' in x:
	db_condition['password'] = hashlib.md5(bytes(x['password'], 'utf-8')).hexdigest()

	db_filter = {
		'_id': False,
		'id': True,
		'admin': True,
		# 'balance': True,
		# 'rating': True,
		'login': True,
		'name': True,
		'surname': True,
		'mail': True,
		'avatar': True,
	}

	res = db['users'].find_one(db_condition, db_filter)

	# Wrong password
	if not res:
		raise ErrorWrong('password')

	# Assignment of the token to the user

	if not this.token:
		raise ErrorAccess('token')

	req = {
		'token': this.token,
		'id': res['id'],
		'time': this.timestamp,
	}
	db['tokens'].insert_one(req)

	# Update online users

	online_update(this.socketio, res, this.token)

	# Response

	res = {
		'id': res['id'],
		'login': res['login'],
		'name': res['name'],
		'surname': res['surname'],
		'avatar': IMAGE['link_opt'] + res['avatar'],
		'admin': res['admin'],
		'mail': res['mail'],
		# 'balance': res['balance'],
		# 'rating': res['rating'],
		'new': new,
	}

	return res

# Log out
# ! Сокет на авторизацию на всех вкладках токена
# ! Перезапись информации этого токена уже в онлайне

def exit(this, **x):
	# Not authorized
	if not this.token:
		raise ErrorAccess('token')

	# Check token
	token = db['tokens'].find_one({'token': this.token}, {'_id': True})

	# Wrong token
	if not token:
		raise ErrorWrong('token')

	# Remove token
	db['tokens'].remove(token['_id'])

	# Close session

	for online in db['online'].find({'token': this.token}):
		online_user_update(online)

		online['id'] = this.token
		online['admin'] = 2

		if 'name' in online:
			del online['name']

		if 'surname' in online:
			del online['surname']

		if 'login' in online:
			del online['login']

		if 'avatar' in online:
			del online['avatar']

		online['start'] = this.timestamp

		db['online'].save(online)

		online_emit_del(this.socketio, this.user['id'])

	# ! Отправлять сокет всем сессиям этого браузера на выход

# Edit personal information

def edit(this, **x):
	# Checking parameters
	check_params(x, (
		('name', False, str),
		('surname', False, str),
		('login', False, str),
		('description', False, str),
		('mail', False, str),
		('password', False, str),
		('avatar', False, str),
		('file', False, str),
		('social', False, list, dict),
	))

	# No access
	if this.user['admin'] < 3:
		raise ErrorAccess('edit')

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
	if 'password' in x and len(x['password']):
		this.user['password'] = process_password(x['password'])

	# Change fields
	for i in ('description', 'mail', 'social'):
		if i in x:
			this.user[i] = x[i]

	# Avatar
	if 'avatar' in x:
		try:
			file_type = x['file'].split('.')[-1]

		# Invalid file extension
		except:
			raise ErrorInvalid('file')

		try:
			link = load_image(x['avatar'], file_type)
			this.user['avatar'] = link

		# Error loading photo
		except:
			raise ErrorUpload('avatar')

	# Save changes
	db['users'].save(this.user)

	# Response

	avatar = IMAGE['link_opt'] + this.user['avatar']

	res = {
		'avatar': avatar,
	}

	return res

# # Recover password

# def recover(this, **x):
# 	# Checking parameters

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