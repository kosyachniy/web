from sets import IMAGE
from api._func.mongodb import db
from api._error import ErrorWrong, ErrorAccess, ErrorBlock
from api._func import check_params, get_user


def get(this, **x):
	# Checking parameters

	check_params(x, (
		('id', False, (int, list), int),
		('count', False, int),
		('fields', False, list, str),
	))

	# Condition formation

	process_one = False

	if 'id' in x:
		if type(x['id']) == int:
			db_condition = {
				'id': x['id'],
			}

			process_one = True

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

	if process_one:
		if x['id'] == this.user['id']:
			process_self = True

	process_moderator = this.user['admin'] >= 5
	process_admin = this.user['admin'] >= 7

	# Get users

	db_filter = {
		'_id': False,
		'id': True,
		'login': True,
		'name': True,
		'surname': True,
		'avatar': True,
		'admin': True,
		# 'balance': True,
		# 'rating': True,
		# 'description': True,
		# 'online': False,
	}

	if process_self:
		db_filter['mail'] = True
		db_filter['phone'] = True
		db_filter['social'] = True
		# db_filter['transactions'] = True

	# if process_moderator:
	# 	db_filter['transactions'] = True

	if process_admin:
		db_filter['phone'] = True
		db_filter['mail'] = True
		db_filter['social'] = True

	#

	users = list(db['users'].find(db_condition, db_filter))
	users = sorted(users, key=lambda i: i['rating'])[::-1]

	# Count

	count = x['count'] if 'count' in x else None
	users = users[:count]

	# Processing

	for i in range(len(users)):
		# Avatar

		users[i]['avatar'] = IMAGE['link_opt'] + users[i]['avatar']

		# # Online

		# users[i]['online'] = db['online'].find_one({'id': users[i]['id']}, {'_id': True}) == True

	# Response

	res = {
		'users': users,
	}

	return res

# Block

def block(this, **x):
	# Checking parameters

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