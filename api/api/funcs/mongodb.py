"""
Database
"""

# Libraries
## System
import json

## External
from pymongo import MongoClient


# Params
with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['mongo']

with open('keys.json', 'r') as file:
    keys = json.loads(file.read())['mongo']


# Global variables
db = MongoClient(
    host=sets['host'],
    port=27017,
    username=keys['login'],
    password=keys['password'],
    authSource='admin',
    authMechanism='SCRAM-SHA-1'
)[sets['db']]
