from func.mongodb import db
from api._error import ErrorEmpty, ErrorAccess
from api._func import check_params


def search(this, **x):
	# Checking parameters

	check_params(x, (
		('cont', True, str),
	))

	# Request preparation

	x['cont'] = x['cont'].lower()

	# Empty request
	if not x['cont']:
		raise ErrorEmpty('cont')

	# Users

	users = []

	db_filter = {
		'_id': False,
		'id': True,
		'login': True,
		'name': True,
		'surname': True,
		'avatar': True,
		'mail': True,
		'description': True,
	}

	for i in db['users'].find({}, db_filter):
		if any(x['cont'] in j.lower() for j in (i['name'], i['surname'], i['mail'], i['description'], i['login'])):
			i['avatar'] = IMAGE['link_opt'] + i['avatar']
			users.append(i)

	# Response

	res = {
		'users': users,
		# 'comments': [],
	}

	return res