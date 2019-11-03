import os
import re
import time
import base64

import requests

from mongodb import db
from api._error import ErrorSpecified, ErrorInvalid, ErrorType

from sets import CLIENT


# Проверить наличие файла по имени

def get_file(url, num):
	url = '/static/' + url + '/'

	for i in os.listdir('app' + url):
		if re.search(r'^' + str(num) + '\.', i):
			return i

	return None

# Ссылка на файл

def get_preview(url, num=0):
	src =  CLIENT['link'] + 'load/' + url + '/'

	file = get_file(url, num)
	if file:
		return src + file

	return src + '0.png'

# ID следующего изображения

def max_image(url):
	x = os.listdir(url)
	k = 0
	for i in x:
		j = re.findall(r'\d+', i)
		if len(j) and int(j[0]) > k:
			k = int(j[0])
	return k+1

# Загрузить изображение

def load_image(url, data, adr=None, format='jpg', type='base64'):
	url = 'app/static/' + url

	if type == 'base64':
		data = base64.b64decode(data)

	if adr:
		for i in os.listdir(url):
			if re.search(r'^' + str(adr) + '\.', i):
				os.remove(url + '/' + i)
	else:
		adr = max_image(url)

	with open('{}/{}.{}'.format(url, str(adr), format), 'wb') as file:
		file.write(data)

	return adr

# Заменить в тексте изображения

def reimg(s):
	k = 0

	while True:
		x = re.search(r'<img ', s[k:])
		if x:
			st = list(x.span())
			st[1] = st[0] + s[k+st[0]:].index('>')
			vs = ''
			if 'src="' in s[k+st[0]:k+st[1]]:
				if re.search(r'image/.*;', s[k+st[0]:k+st[1]]) and 'base64,' in s[k+st[0]:k+st[1]]:
					start = k + st[0] + s[k+st[0]:].index('base64,') + 7
					stop = start + s[start:].index('"')

					b64 = s[start:stop]
					form = re.search(r'image/.*;', s[k+st[0]:start]).group(0)[6:-1]
					adr = load_image('', b64, format=form)

					vs = '<img src="/load/{}.{}">'.format(adr, form)
				else:
					start = k + re.search(r'src=".*', s[k:]).span()[0] + 5
					stop = start + s[start:].index('"')
					href = s[start:stop]

					if href[:5] == '/load':
						href = CLIENT['link'] + href[1:]
					if href[:4] == 'http':
						b64 = str(base64.b64encode(requests.get(href).content))[2:-1]
						form = href.split('.')[-1]
						if 'latex' in form or '/' in form or len(form) > 5:
							form = 'png'
						adr = load_image('', b64, format=form)

						vs = '<img src="/load/{}.{}">'.format(adr, form)

			if vs:
				s = s[:k+st[0]] + vs + s[k+st[1]+1:]
				k += st[0] + len(vs)
			else:
				k += st[1]
		else:
			break

	return s

# Получить пользователя

def get_user(id):
	if id:
		db_condition = {
			'id': id,
		}

		db_filter = {
			'_id': False,
			'id': True,
			'login': True,
			'name': True,
			'surname': True,
		}
	
		user_req = db['users'].find_one(db_condition, db_filter)

		user_req['avatar'] = get_preview('users', user_req['id'])
	else:
		user_req = 0

	return user_req

# Проверка параметров

def check_params(x, filters): # ! Удалять другие поля (которых нет в списке)
	for i in filters:
		if i[0] in x:
			# Неправильный тип данных
			if type(i[2]) not in (list, tuple):
				el_type = (i[2],)
			else:
				el_type = i[2]

			cond_type = type(x[i[0]]) not in el_type
			cond_iter = type(x[i[0]]) in (tuple, list)

			try:
				cond_iter_el = cond_iter and any(type(j) != i[3] for j in x[i[0]])
			except:
				raise ErrorType(i[0])

			if cond_type or cond_iter_el:
				raise ErrorType(i[0])
				# return dumps({'error': 4, 'message': ERROR[3].format(i[0], str(i[2]))})

			cond_null = type(i[-1]) == bool and i[-1] and cond_iter and not len(x[i[0]])
			
			if cond_null:
				raise ErrorInvalid(i[0])

		# Не все поля заполнены
		elif i[1]:
			raise ErrorSpecified(i[0])
			# return dumps({'error': 3, 'message': ERROR[2].format(i[0])})

# Следующий ID БД

def next_id(name):
	try:
		db_filter = {'id': True, '_id': False}
		id = db[name].find({}, db_filter).sort('id', -1)[0]['id'] + 1
	except:
		id = 1
	
	return id

# Преобразовать язык в код

def get_language(name):
	languages = ('en', 'ru', 'fi', 'es')

	if name in languages:
		name = languages.index(name)
	
	elif name not in range(len(languages)):
		name = 0

	return name

# Получить доступный статус для пользователя

def get_status(user):
	if user['admin'] >= 6:
		return 0
	elif user['admin'] >= 5:
		return 1
	elif user['admin'] >= 3:
		return 3
	
	return 3 # !

def get_status_condition(user):
	if user['id']:
		return {
			'$or': [{
				'status': {'$gte': get_status(user)},
			}, {
				'user': user['id'],
			}]
		}

	else:
		return {
			'status': {'$gte': get_status(user)},
		}

# Определить пользователя по sid

def get_id(sid):
	db_filter = {
		'_id': False,
		'user': True,
	}

	user = db['online'].find_one({'sid': sid}, db_filter)

	if not user:
		raise Exception('sid not found')
	
	return user['user']

# Все sid этого пользователя

def get_sids(user):
	db_filter = {
		'_id': False,
		'sid': True,
	}

	user_sessions = db['online'].find({'user': user}, db_filter)
	
	return [i['sid'] for i in user_sessions]

# Получить дату из timestamp

def get_date(x, template='%Y%m%d'):
	return time.strftime(template, time.localtime(x))