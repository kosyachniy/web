import json

from pymongo import MongoClient


with open('keys.json', 'r') as file:
	MONGO = json.loads(file.read())['mongo']

db = MongoClient(
	username=MONGO['login'],
	password=MONGO['password'],
	authSource='admin',
	authMechanism='SCRAM-SHA-1'
)[MONGO['db']]