from mongodb import db
from api._error import ErrorEmpty
from api._func import check_params, get_preview


def search(this, **x):
	# Проверка параметров

	check_params(x, (
		('token', False, str),
		('cont', True, str),
	))

	#

	x['cont'] = x['cont'].lower()

	# Пустой запрос

	if not x['cont']:
		raise ErrorEmpty('cont')
		# return dumps({'error': 6, 'message': ERROR[34]})

	# Пользователи

	users = []

	db_filter = {
		'_id': False,
		'name': True,
		'surname': True,
		'mail': True,
		'description': True,
		'id': True,
		'login': True,
	}

	for i in db['users'].find({}, db_filter):
		if any(x['cont'] in j.lower() for j in (i['name'], i['surname'], i['mail'], i['description'], i['login'])):
			i['avatar'] = get_preview('users', i['id'])
			users.append(i)

	# Леддеры

	ladders = []
	db_filter = {
		'_id': False,
		'name': True,
		'description': True,
		'comment': True,
		'tags': True,
		'id': True,
		'steps.options.complete': True,
	}
	for i in db['ladders'].find({}, db_filter):
		if any(x['cont'] in j.lower() for j in (i['name'], i['description'])) or any(x['cont'] in j.lower() for j in i['tags']) or any(x['cont'] in j.lower() for j in i['comment']):
			i['cover'] = get_preview('ladders', i['id'])
			ladders.append(i)

	if len(ladders):
		for i in range(len(ladders)):
			ladders[i]['complete'] = 0
			for j in ladders[i]['steps']:
				for u in j['options']:
					ladders[i]['complete'] += len(u['complete'])

		ladders.sort(key=lambda i: i['complete'], reverse=-1)

		for i in range(len(ladders)):
			del ladders[i]['steps']
			del ladders[i]['complete']

	# Степы

	steps = []
	db_filter = {
		'_id': False,
		'id': True,
		'steps.name': True,
		'steps.options.cont': True,
		'steps.options.answer.type': True,
		'steps.theory': True,
		'steps.options.answer.cont': True,
		'steps.id': True,
		# 'steps.comment': True,
	}
	status = 3 if this.user['admin'] < 5 else 1

	for i in db['ladders'].find({'status': {'$gte': status}}, db_filter):
		for j in i['steps']:
			cond_main = any(x['cont'] in u.lower() for u in (j['name'], j['theory']))
			cond_cont = any(x['cont'] in u['cont'].lower() for u in j['options'])

			answer_all = []
			for u in j['options']:
				if u['answer']['type'] == 'field' and 'cont' in u['answer']:
					for t in u['answer']['cont']:
						answer_all.append(t)
			cond_answer = x['cont'] in answer_all

			if cond_main or cond_cont or cond_answer:
				j['ladder'] = i['id']
				steps.append(j)

	res = {
		'users': users,
		'ladders': ladders,
		'steps': steps,
		'comments': [],
	}

	return res