from pymongo import MongoClient


try:
	from keys import DB

except:
	db = MongoClient()['uple']

else:
	db = MongoClient(
		username=DB['login'],
		password=DB['password'],
		authSource='admin',
		authMechanism='SCRAM-SHA-1'
	)[DB['name']]


check = db['posts'].find_one({}, {'_id': True})

if not check:
	post = {
		'id': 1,
		'name': 'Тест',
		'cont': 'Содержание..',
		'tags': ['Маркетинг',],
	}

	db['posts'].insert_one(post)