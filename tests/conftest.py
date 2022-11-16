import sys
import os

os.chdir(os.getcwd()+'/api/')
sys.path.append(os.getcwd())

os.environ['PROJECT_NAME'] = 'test'
os.environ['SERVER'] = 'http://localhost/api/'
os.environ['CLIENT'] = 'http://localhost/'
os.environ['MODE'] = 'test'
os.environ['MONGO_HOST'] = 'localhost:27017'
os.environ['MONGO_USER'] = 'test'
os.environ['MONGO_PASS'] = 'test'
os.environ['TG_TOKEN'] = '123456789:AABBCCDDEEFFaabbccddeeff-1234567890'
