from flask import Flask
from params import LINK

# import logging


# logging.basicConfig(filename='error.log',level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')


from app import api

from app import index