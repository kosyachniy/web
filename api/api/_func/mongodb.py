import json

from pymongo import MongoClient


from sets import DB

with open('keys.json', 'r') as file:
	MONGO = json.loads(file.read())['mongo']

db = MongoClient(
	host=DB['hostname'],
	port=27017,
	username=MONGO['login'],
	password=MONGO['password'],
	authSource='admin',
	authMechanism='SCRAM-SHA-1'
)[DB['name']]