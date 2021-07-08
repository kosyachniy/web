"""
Types checking functionality for the API
"""

from functools import wraps

from pydantic import BaseModel as BaseType
from pydantic.error_wrappers import ValidationError

from ..errors import ErrorSpecified, ErrorType


def _prepare(data):
    """ Remove extra indentation """

    for i in data:
        if isinstance(data[i], str):
            data[i] = data[i].strip()

        elif isinstance(data[i], (list, dict)):
            for j in data[i]:
                if isinstance(data[i][j], str):
                    data[i][j] = data[i][j].strip()

    return data

def _check(params, filters):
    """ Convert the parameters to the required object """

    try:
        return filters(**params)

    except ValidationError as e:
        param_name = e.errors()[0]['loc'][0]

        if param_name in params:
            raise ErrorType(param_name)

        raise ErrorSpecified(param_name)


def validate(filters):
    """ Validation of function parameters """

    def decorator(f):
        @wraps(f)
        def wrapper(this, params):
            params = _prepare(params)
            params = _check(params, filters)
            return f(this, params)
        return wrapper
    return decorator
