import time

from func.mongodb import db
from api._error import ErrorInvalid, ErrorAccess
from api._func import reimg, get_user, check_params, next_id


# Add

def add(this, **x):
	# Checking parameters

	check_params(x, (
		('name', True, str),
		('cont', True, str),
	))

	#

	query = {
		'id': next_id('feedback'),
		'name': x['name'],
		'cont': reimg(x['cont']),
		'user': this.user['id'],
		'time': this.timestamp,
		'success': 0,
	}

	db['feedback'].insert(query)

	# Response

	res = {
		'id': query['id'],
	}

	return res

# Get

def get(this, **x):
	# Checking parameters

	check_params(x, (
		('count', False, int),
	))

	# No access

	if this.user['admin'] < 4:
		raise ErrorAccess('token')

	# Get news

	count = x['count'] if 'count' in x else None

	news = list(db['feedback'].find({}, {'_id': False}).sort('time', -1)[0:count])

	for i in range(len(news)):
		news[i]['user'] = get_user(news[i]['user'])

	# Response

	res = {
		'feedback': news,
	}

	return res

# Delete

def delete(this, **x):
	# Checking parameters
	check_params(x, (
		('id', True, int),
	))

	# No access
	if this.user['admin'] < 5:
		raise ErrorAccess('token')

	# Get feedback

	feedback = db['feedback'].find_one({'id': x['id']}, {'_id': True})

	## Wrong ID
	if not feedback:
		raise ErrorWrong('id')

	# Remove feedback
	db['feedback'].remove(feedback['_id'])