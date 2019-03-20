from flask import Flask, session

# import logging


# logging.basicConfig(filename='error.log',level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')

# Мультиязычность

from flask_babel import Babel
babel = Babel(app)

@babel.localeselector
def get_locale(request):
	if 'lang' not in session:
		session['lang'] = request.accept_languages.best_match(['en', 'ru']) or 'en'
	return session['lang']


from app import api

from app import index