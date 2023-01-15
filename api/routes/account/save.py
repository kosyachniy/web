"""
The editing method of the account object of the API
"""

from copy import deepcopy

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.track import Track
from services.auth import sign


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
    locale: str = None
    mailing: dict = None

@router.post("/save/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Save personal information """

    # No access
    if user.status < 3:
        raise ErrorAccess('save')

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
        token=request.state.token,
        ip=request.state.ip,
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
