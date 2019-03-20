CSRF_ENABLED = True

SECRET_KEY = 'cheta-nuzhno-zdes-napisat'

class BaseConfig(object):
	SUPPORTED_LANGUAGES = {'en': 'English', 'ru': 'Russian'}
	BABEL_DEFAULT_LOCALE = 'en'
	BABEL_DEFAULT_TIMEZONE = 'UTC'