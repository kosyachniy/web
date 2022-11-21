"""
The creating method of the payment object of the API
"""

from typing import Union

from fastapi import APIRouter # , Body, Depends
from pydantic import BaseModel
# from consys.handlers import pre_process_phone

# from models.user import User
# from services.request import get_request
# from routes.account.auth import reg
# from routes.promos.invite import get_promo
# from lib.pay import create


router = APIRouter()


class Type(BaseModel):
    user: int = None
    login: Union[int, str] = None
    promo: str = None
    value: int
    # NOTE: For general authorization method fields
    name: str = None
    surname: str = None

@router.post("/create/")
async def handler(
    # data: Type = Body(...),
    # request = Depends(get_request),
):
    """ Create a payment request """

    # if data.login:
    #     phone = pre_process_phone(data.login) # TODO: optimize
    #     users = User.get(phone=phone, fields={})

    #     if not users:
    #         user = await reg(request, data, 'phone', 'payment')
    #     else:
    #         user = users[0]

    # elif data.user:
    #     user = User.get(data.user)

    # else:
    #     user = request.user

    # # if data.promo:
    # #     promo = get_promo(data.promo)

    # #     if promo.discount:
    # #         user.discount = promo.discount
    # #         user.save()

    # #         promo.users.append(user.id)
    # #         promo.save()

    # # TODO: change default text
    # token = create(data.value, 'Оплата подписки', {'user': user.id})
    # return {'token': token}
