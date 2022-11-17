import sys
import os

os.chdir(os.getcwd()+'/api/')
sys.path.append(os.getcwd())

os.environ['PROJECT_NAME'] = 'test'
os.environ['SERVER'] = 'http://localhost/api/'
os.environ['CLIENT'] = 'http://localhost/'
os.environ['MODE'] = 'test'
os.environ['TG_TOKEN'] = '123456789:AABBCCDDEEFFaabbccddeeff-1234567890'
