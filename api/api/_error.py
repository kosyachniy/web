# Не все параметры

class ErrorSpecified(Exception):
	def __init__(self, par):
		self.txt = par

# Занято

class ErrorBusy(Exception):
	def __init__(self, par):
		self.txt = par

# Недопустимый

class ErrorInvalid(Exception):
	def __init__(self, par):
		self.txt = par

# Неправильный

class ErrorWrong(Exception):
	def __init__(self, par):
		self.txt = par

# Загрузка на сервер

class ErrorUpload(Exception):
	def __init__(self, par):
		self.txt = par

# Нет прав

class ErrorAccess(Exception):
	def __init__(self, par):
		self.txt = par

# Нечего отображать

class ErrorEmpty(Exception):
	def __init__(self, par):
		self.txt = par

# Недостаточно

class ErrorEnough(Exception):
	def __init__(self, par):
		self.txt = par

#  Заблокирован

class ErrorBlock(Exception):
	def __init__(self, par):
		self.txt = par

#  Неправильный тип данных

class ErrorType(Exception):
	def __init__(self, par):
		self.txt = par