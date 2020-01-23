from func.mongodb import db
from api._error import ErrorWrong, ErrorAccess, ErrorBlock
from api._func import check_params, get_preview, get_user


def get(this, **x):
	# Verification of parameters

	check_params(x, (
		('id', False, (int, list, tuple), int),
		('count', False, int),
	))

	# Condition formation

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

	# Advanced options

	process_self = False

	if 'id' in x and type(x['id']) == int:
		if x['id'] == this.user['id']:
			process_self = True

	# Get users

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

	# Count

	count = x['count'] if 'count' in x else None
	users = users[:count]

	# Processing

	for i in range(len(users)):
		# Avatar

		users[i]['avatar'] = get_preview('users', users[i]['id'])

		# # Online

		# users[i]['online'] = db['online'].find_one({'user': users[i]['id']}, {'_id': True}) == True

	# Response

	res = {
		'users': users,
	}

	return res

# Block

def block(this, **x):
	# Verification of parameters

	check_params(x, (
		('id', True, int),
	))

	# Get user

	users = db['users'].find_one({'id': x['id']})

	## Wrond ID
	if not users:
		raise ErrorWrong('id')

	# No access
	if this.user['admin'] < 6 or users['admin'] > this.user['admin']:
		raise ErrorAccess('block')

	# Change status
	users['admin'] = 1

	# Save
	db['users'].save(users)