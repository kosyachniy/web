"""
Types checking functionality for the API
"""

from functools import wraps

from pydantic import BaseModel as BaseType
from pydantic.error_wrappers import ValidationError
from consys.errors import ErrorSpecified, ErrorType


def _strip(data):
    """ Remove extra indentation """

    if not isinstance(data, dict):
        return

    for field in set(data):
        if isinstance(data[field], str):
            data[field] = data[field].strip()
            continue

        if isinstance(data[field], dict):
            _strip(data[field])
            continue

        if isinstance(data[field], (list, tuple, set)):
            for el in data[field]:
                _strip(el)

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
            _strip(data)
            data = _check(data, filters)
            return f(this, request, data)
        return wrapper
    return decorator
