from pymongo import MongoClient

from keys import DB


db = MongoClient(
	username=DB['login'],
	password=DB['password'],
	authSource='admin',
	authMechanism='SCRAM-SHA-1'
)['uple']