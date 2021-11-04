"""
The cancel method of the payment object of the API
"""

from consys.errors import ErrorAccess, ErrorRepeat

from api.lib import BaseType, validate


class Type(BaseType):
    pass

@validate(Type)
async def handle(request, data):
    """ Delete payments data """

    # No access
    if request.user.status < 3:
        raise ErrorAccess('cancel')

    # No payment data
    if not request.user.pay:
        raise ErrorRepeat('cancel')

    del request.user.pay
    request.user.save()
