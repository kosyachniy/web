import time

from mongodb import db
from api._error import ErrorInvalid, ErrorAccess
from api._func import reimg, get_user, check_params


# Получение

def get(this, **x):
	# Проверка параметров

	check_params(x, (
		('id', False, (int, list, tuple), int),
		('count', False, int),
		('category', False, int),
		('language', False, (int, str)),
	))

	# Язык

	if 'language' in x:
		x['language'] = get_language(x['language'])
	else:
		x['language'] = this.language

	#

	count = x['count'] if 'count' in x else None

	###

	res = {
		'articles': [{
			'name': 'Название',
			'cont': 'Содержание',
			'tags': ['Программирование', 'Маркетинг'],
		}]
	}

	return res