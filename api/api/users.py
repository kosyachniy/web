from mongodb import db
from api._error import ErrorWrong, ErrorAccess, ErrorBlock
from api._func import check_params, get_preview, get_user


def get(this, **x):
	# Проверка параметров

	check_params(x, (
		('id', False, (int, list, tuple), int),
		('count', False, int),
	))

	#

	count = x['count'] if 'count' in x else None

	if 'id' in x:
		if type(x['id']) == int:
			db_condition = {
				'id': x['id'],
			}

		else:
			db_condition = {
				'id': {'$in': x['id']},
			}

	else:
		db_condition = {
			'admin': {'$gte': 3},
		}
	
	# Расширенные параметры

	process_self = False

	if 'id' in x and type(x['id']) == int:
		if x['id'] == this.user['id']:
			process_self = True

	#

	db_filter = {
		'_id': False,
		'id': True,
		'name': True,
		'surname': True,
		'login': True,
		'rating': True,
		'description': True,
		'admin': True,
		# 'online': False, # !
	}

	if process_self:
		db_filter['mail'] = True
		db_filter['templates'] = True
		db_filter['social'] = True
		# db_filter['transactions'] = True

	users = list(db['users'].find(db_condition, db_filter))
	users = sorted(users, key=lambda i: i['rating'])[::-1]

	# Количество

	users = users[:count]

	for i in range(len(users)):
		# # Транзакции

		# if 'transactions' in users[i]:
		# 	users[i]['transactions'] = users[i]['transactions'][::-1]

		# 	for j in range(len(users[i]['transactions'])):
		# 		us = get_user(users[i]['transactions'][j]['user'])
		# 		users[i]['transactions'][j]['user'] = us if us else {'id': 0}

		# Аватарка
		
		users[i]['avatar'] = get_preview('users', users[i]['id'])
	
		# # Онлайн

		# users[i]['online'] = db['online'].find_one({'user': users[i]['id']}, {'_id': True}) == True

	# # Пользователь заблокирован

	# if users['admin'] < 3 and this.user['admin'] < 6:
	# 	raise ErrorBlock('user')
	# 	# return dumps({'error': 7, 'message': ERROR[32]})

	# # Список леддеров # ! Только если отправлен запрос на необходимость

	# ladders = {str(i): [] for i in users['ladders']}
	# # for i in users['steps']:
	# # 	s = str(i['ladder'])

	# # 	if s in ladders:
	# # 		ladders[s].append(i['step'])
	# # 	else:
	# # 		ladders[s] = [i['step'],]

	# db_ladders_filter = {
	# 	'_id': False,
	# 	'steps': True,
	# 	'name': True,
	# }

	# db_steps_filter = {
	# 	'_id': False,
	# 	'id': True,
	# 	'status': True,
	# }

	# for i in ladders:
	# 	ladder = db['ladders'].find_one({'id': int(i)}, db_ladders_filter)

	# 	# Степы

	# 	for j in range(len(ladder['steps'])):
	# 		db_condition = {'id': ladder['steps'][j]}
	# 		step = db['steps'].find_one(db_condition, db_steps_filter)
	# 		ladder['steps'][j] = step

	# 	#

	# 	step_all_published = [j['id'] for j in ladder['steps'] if j['status'] >= 3]
	# 	# print(step_all_published, users['steps'])

	# 	for j in users['steps']:
	# 		if j['step'] in step_all_published:
	# 			ladders[i].append(j['step'])

	# 	j = 0
	# 	while j < len(ladders[i]):
	# 		if ladders[i][j] not in step_all_published:
	# 			del ladders[i][j]
	# 		else:
	# 			j += 1

	# 	ladders[i] = {
	# 		'name': ladder['name'],
	# 		'steps': ladders[i],
	# 		'complete': len(set(ladders[i]) & set(step_all_published)),
	# 		'all': len(step_all_published)
	# 	}

	# users['ladders'] = ladders

	# Ответ

	res = {
		'users': users,
	}

	return res

#

def block(this, **x):
	# Проверка параметров

	check_params(x, (
		('id', True, int),
	))

	#

	users = db['users'].find_one({'id': x['id']})

	# Неправильный пользователь

	if not users:
		raise ErrorWrong('user')

	# Нет прав на блокировку

	if this.user['admin'] < 6 or users['admin'] > this.user['admin']:
		raise ErrorAccess('block')

	users['admin'] = 1
	db['users'].save(users)