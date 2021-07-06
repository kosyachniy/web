"""
Types checking functionality for the API
"""

from functools import wraps

from pydantic import BaseModel as BaseType
from pydantic.error_wrappers import ValidationError

from ..errors import ErrorSpecified, ErrorType


def _check_params(params, filters):
    try:
        return filters(**params)

    except ValidationError as e:
        param_name = e.errors()[0]['loc'][0]

        if param_name in params:
            raise ErrorType(param_name)

        raise ErrorSpecified(param_name)


def validate(filters):
    def decorator(f):
        @wraps(f)
        def wrapper(this, **params):
            params = _check_params(params, filters)
            return f(this, params)
        return wrapper
    return decorator
