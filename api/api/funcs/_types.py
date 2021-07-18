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

def _check(data, filters):
    """ Convert the parameters to the required object """

    try:
        return filters(**data)

    except ValidationError as e:
        field = e.errors()[0]['loc'][0]

        if field in data:
            raise ErrorType(field)

        raise ErrorSpecified(field)


def validate(filters):
    """ Validation of function parameters """

    def decorator(f):
        @wraps(f)
        def wrapper(this, request, data):
            data = _prepare(data)
            data = _check(data, filters)
            return f(this, request, data)
        return wrapper
    return decorator
