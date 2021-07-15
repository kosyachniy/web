"""
Errors of the API
"""

class BaseError(Exception):
    """ Base error """

    def __init__(self, par):
        self.txt = par
        self._code = -1

    @property
    def code(self):
        raise AttributeError('Base class hasn\'t its own code!')

class ErrorSpecified(BaseError):
    """ Not all parameters """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 4

class ErrorBusy(BaseError):
    """ Busy """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 5

class ErrorInvalid(BaseError):
    """ Invalid (Does not pass the criteria) """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 6

class ErrorWrong(BaseError):
    """ Wrong (Passes the criteria, but is incorrect) """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 7

class ErrorUpload(BaseError):
    """ Uploading to the server """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 8

class ErrorAccess(BaseError):
    """ No rights """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 9

class ErrorEmpty(BaseError):
    """ Nothing to display """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 10

class ErrorEnough(BaseError):
    """ Not enough """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 11

class ErrorBlock(BaseError):
    """ Blocked """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 12

class ErrorType(BaseError):
    """ Incorrect data type """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 13

class ErrorCount(BaseError):
    """ Quantity limit """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 14

class ErrorRepeat(BaseError): # TODO: Already / Duplicate
    """ Duplicate """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 15

class ErrorTime(BaseError):
    """ Time expired """

    def __init__(self, par):
        super().__init__(par)

    @property
    def code(self):
        return self._code

    @code.getter
    def code(self):
        return 16
