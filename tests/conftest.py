import sys
import os

os.chdir(os.getcwd()+'/api/')
sys.path.append(os.getcwd())

os.environ["PROJECT_NAME"] = 'web'
os.environ["SERVER"] = 'http://localhost/api/'
os.environ["CLIENT"] = 'http://localhost/'
os.environ["MODE"] = 'test'
os.environ["MONGO_HOST"] = 'localhost:27017'
os.environ["TG_TOKEN"] = '123456789:AABBCCDDEEFFaabbccddeeff-1234567890'
