import os
import re
import time
import base64

import requests
from PIL import Image, ExifTags

from func.mongodb import db
from api._error import ErrorSpecified, ErrorInvalid, ErrorType

from sets import IMAGE


WIDTH_OPTIMIZED = 700


# Check existence the file by name

def get_file(url, num):
	for i in os.listdir('../data/load/{}/'.format(url)):
		if re.search(r'^' + str(num) + '\.', i):
			return i

	return None

# Image link

def get_preview(num=0, url=''):
	src = IMAGE['link_opt']
	if url:
		src += url + '/'

	file = get_file(url, num)
	if file:
		return src + file

	return src + '0.png'

# Next image ID

def max_image(url):
	x = os.listdir(url)
	k = 0
	for i in x:
		j = re.findall(r'\d+', i)
		if len(j) and int(j[0]) > k:
			k = int(j[0])
	return k+1

# Upload image

def load_image(url, data, adr=None, format='jpg', type='base64'):
	url_opt = '../data/load/opt/' + url
	url = '../data/load/' + url

	if type == 'base64':
		data = base64.b64decode(data)

	if adr:
		for i in os.listdir(url):
			if re.search(r'^' + str(adr) + '\.', i):
				os.remove(url + '/' + i)

		for i in os.listdir(url_opt):
			if re.search(r'^' + str(adr) + '\.', i):
				os.remove(url_opt + '/' + i)
	else:
		adr = max_image(url)

	link = '{}/{}.{}'.format(url, adr, format)
	link_opt = '{}/{}.{}'.format(url_opt, adr, format)

	with open(link, 'wb') as file:
		file.write(data)

	# EXIF data

	try:
		image=Image.open(link)
		for orientation in ExifTags.TAGS.keys():
			if ExifTags.TAGS[orientation]=='Orientation':
				break
		exif=dict(image._getexif().items())

		if exif[orientation] == 3:
			image=image.transpose(Image.ROTATE_180)
		elif exif[orientation] == 6:
			image=image.transpose(Image.ROTATE_270)
		elif exif[orientation] == 8:
			image=image.transpose(Image.ROTATE_90)
		image.save(link)
		image.close()

	except (AttributeError, KeyError, IndexError):
		# cases: image don't have getexif
		pass

	# Оптимизированная версия

	try:
		img = Image.open(link)

		wpercent = (WIDTH_OPTIMIZED / float(img.size[0]))
		hsize = int((float(img.size[1]) * float(wpercent)))
		img = img.resize((WIDTH_OPTIMIZED, hsize), Image.ANTIALIAS)

		img.save(link_opt)

	except:
		with open(link_opt, 'wb') as file:
			file.write(data)

	return adr

# Replace image in text

def reimg(s):
	k = 0

	while True:
		x = re.search(r'<img ', s[k:])
		if x:
			st = list(x.span())
			st[1] = st[0] + s[k+st[0]:].index('>')
			vs = ''
			if 'src=' in s[k+st[0]:k+st[1]]:
				if re.search(r'image/.*;', s[k+st[0]:k+st[1]]) and 'base64,' in s[k+st[0]:k+st[1]]:
					start = k + st[0] + s[k+st[0]:].index('base64,') + 7
					try:
						stop = start + s[start:].index('"')
					except:
						stop = start + s[start:].index('\'')

					b64 = s[start:stop]
					form = re.search(r'image/.*;', s[k+st[0]:start]).group(0)[6:-1]
					adr = load_image('', b64, format=form)

					# vs = '<img src="/load/{}.{}">'.format(adr, form)
					vs = '<img src="/load/opt/{}.{}">'.format(adr, form)
				else:
					start = k + re.search(r'src=.*', s[k:]).span()[0] + 5
					try:
						stop = start + s[start:].index('"')
					except:
						stop = start + s[start:].index('\'')

					href = s[start:stop]

					if href[:5] == '/load': # !
						href = IMAGE['link'] + href[5:]
					if href[:4] == 'http':
						b64 = str(base64.b64encode(requests.get(href).content))[2:-1]
						form = href.split('.')[-1]
						if 'latex' in form or '/' in form or len(form) > 5:
							form = 'png'
						adr = load_image('', b64, format=form)

						# vs = '<img src="/load/{}.{}">'.format(adr, form)
						vs = '<img src="/load/opt/{}.{}">'.format(adr, form)

			if vs:
				s = s[:k+st[0]] + vs + s[k+st[1]+1:]
				k += st[0] + len(vs)
			else:
				k += st[1]
		else:
			break

	return s

# Get user

def get_user(user_id):
	if user_id:
		db_condition = {
			'id': user_id,
		}

		db_filter = {
			'_id': False,
			'id': True,
			'login': True,
			'name': True,
			'surname': True,
		}

		user_req = db['users'].find_one(db_condition, db_filter)

		user_req['avatar'] = get_preview(user_req['id'], 'users')
	else:
		user_req = 0

	return user_req

# Checking parameters

def check_params(x, filters): # ! Удалять другие поля (которых нет в списке)
	for i in filters:
		if i[0] in x:
			# Invalid data type
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

			cond_null = type(i[-1]) == bool and i[-1] and cond_iter and not len(x[i[0]])

			if cond_null:
				raise ErrorInvalid(i[0])

		# Not all fields are filled
		elif i[1]:
			raise ErrorSpecified(i[0])

# Next DB ID

def next_id(name):
	try:
		db_filter = {'id': True, '_id': False}
		id = db[name].find({}, db_filter).sort('id', -1)[0]['id'] + 1
	except:
		id = 1

	return id

# Convert language to code

def get_language(name):
	languages = ('en', 'ru', 'fi', 'es')

	if name in languages:
		name = languages.index(name)

	elif name not in range(len(languages)):
		name = 0

	return name

# Get available status for user

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

# Define user by sid

def get_id(sid):
	db_filter = {
		'_id': False,
		'id': True,
	}

	user = db['online'].find_one({'sid': sid}, db_filter)

	if not user:
		raise Exception('sid not found')

	# ?
	if type(user['id']) != int or not user['id']:
		return 0

	return user['id']

# All sid of this user

def get_sids(user):
	db_filter = {
		'_id': False,
		'sid': True,
	}

	user_sessions = db['online'].find({'id': user}, db_filter)

	return [i['sid'] for i in user_sessions]

# Get date from timestamp

def get_date(x, template='%Y%m%d'):
	return time.strftime(template, time.localtime(x))

# Leave only the required fields for objects in the list

def reduce_params(cont, params):
	def only_params(el):
		return {i: el[i] for i in params}

	return list(map(only_params, cont))

# Checking how long has been online

def online_back(user_id):
	online = db['online'].find_one({'id': user_id}, {'_id': True})
	if online:
		return 0

	db_filter = {'_id': False, 'online.stop': True}
	user = db['users'].find_one({'id': user_id}, db_filter)['online']

	last = max(i['stop'] for i in user)
	return time.time() - last

# Other sessions of this user

def other_sessions(user_id):
	db_filter = {
		'_id': False,
		'id': True,
	}

	already = db['online'].find_one({'id': user_id}, db_filter)

	return bool(already)
