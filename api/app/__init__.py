from flask import Flask
from flask_cors import CORS

from sets import SERVER, CLIENT

# Логирование

# import logging
# logging.basicConfig(filename='error.log', level=logging.DEBUG)

#

app = Flask(__name__)
app.config.from_object('config')
CORS(app, resources={r'/*': {'origins': '*'}})


from app import api