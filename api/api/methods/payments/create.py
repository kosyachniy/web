"""
The creating method of the payment object of the API
"""

from typing import Union

from consys.handlers import pre_process_phone

from api.lib import BaseType, validate
from api.lib.pay import create
from api.models.user import User
from api.methods.account.auth import reg
# from api.methods.promos.invite import get_promo


class Type(BaseType):
    user: int = None
    login: Union[int, str] = None
    promo: str = None
    value: int

    # NOTE: For general authorization method fields
    name: str = None
    surname: str = None

@validate(Type)
async def handle(request, data):
    """ Create a payment request """

    if data.login:
        phone = pre_process_phone(data.login) # TODO: optimize
        users = User.get(phone=phone, fields={})

        if not users:
            user = await reg(request, data, 'phone', 'payment')
        else:
            user = users[0]

    elif data.user:
        user = User.get(data.user)

    else:
        user = request.user

    # if data.promo:
    #     promo = get_promo(data.promo)

    #     if promo.discount:
    #         user.discount = promo.discount
    #         user.save()

    #         promo.users.append(user.id)
    #         promo.save()

    # TODO: change default text
    token = create(data.value, 'Оплата подписки', {'user': user.id})
    return {'token': token}
