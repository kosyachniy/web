class BaseError(Exception):
	def __init__(self, par):
		self.txt = par
		self._code = -1

	@property
	def code(self):
		raise AttributeError('Base class hasn\'t its own code!')

# Не все параметры

class ErrorSpecified(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 4

# Занято

class ErrorBusy(BaseError):
	def __init__(self, par):
		super().__init__(par)

	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 5

# Недопустимый
# Не проходит по критерям

class ErrorInvalid(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 6

# Неправильный
# Проходит по критериям, но неверный

class ErrorWrong(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 7

# Загрузка на сервер

class ErrorUpload(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 8

# Нет прав

class ErrorAccess(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 9

# Нечего отображать

class ErrorEmpty(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 10

# Недостаточно

class ErrorEnough(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 11

# Заблокирован

class ErrorBlock(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 12

# Неправильный тип данных

class ErrorType(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 13

# Ограничение количества

class ErrorCount(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 14

# Повторное действие

class ErrorRepeat(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 15

# Истекло время

class ErrorTime(BaseError):
	def __init__(self, par):
		super().__init__(par)
		
	@property
	def code(self):
		return self._code

	@code.getter
	def code(self):
		return 16