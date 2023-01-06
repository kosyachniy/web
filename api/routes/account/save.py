"""
The editing method of the account object of the API
"""

from typing import Union
from copy import deepcopy

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.user import User
from models.track import Track
from services.request import get_request


router = APIRouter()


class Type(BaseModel):
    login: str = None
    password: str = None
    image: str = None
    name: str = None
    surname: str = None
    phone: str = None
    mail: str = None
    social: list[dict] = None
    description: str = None
    locale: Union[str, int] = None
    mailing: dict = None

@router.post("/save/")
async def handler(
    data: Type = Body(...),
    request = Depends(get_request),
):
    """ Save personal information """

    # No access
    if request.user.status < 3:
        raise ErrorAccess('save')

    # Get
    user = User.get(ids=request.user.id)

    # Change fields
    # TODO: Fix exceptions on bad fields

    user.login = data.login
    user.password = data.password
    user.image = data.image
    user.name = data.name
    user.surname = data.surname

    phone_old = deepcopy(user.phone)
    user.phone = data.phone
    if phone_old != user.phone:
        user.phone_verified = False

    user.mail = data.mail
    user.social = data.social # TODO: checking
    user.description = data.description
    user.locale = data.locale

    user.mailing = data.mailing

    # Action tracking
    Track(
        title='acc_save',
        data={'fields': [k for k, v in data.dict().items() if v is not None]},
        user=user.id,
        token=request.token,
    ).save()

    # Save
    user.save()

    # Processing
    ## Avatar
    image = None
    if data.image != user.image:
        image = user.image

    ## Phone
    phone = None
    if phone_old != user.phone:
        phone = user.phone

    # Response
    return {
        'image':  image,
        'phone':  phone,
    }