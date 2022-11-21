"""
The authorization via social networks method of the account object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorWrong, ErrorAccess

from models.user import User # process_lower
from models.token import Token
from models.track import Track
from services.request import get_request
from routes.account.auth import reg
from lib import report


router = APIRouter()


class Type(BaseModel):
    user: int
    login: str = None
    name: str = None
    surname: str = None
    utm: str = None

@router.post("/bot/")
async def handler(
    data: Type = Body(...),
    request = Depends(get_request),
):
    """ By bot """

    # TODO: image
    # TODO: the same token

    # No access
    if request.user.status < 2:
        raise ErrorAccess('social')

    fields = {
        'id',
        'login',
        'image',
        'name',
        'surname',
        'title',
        'phone',
        'mail',
        'social',
        'status',
        # 'subscription',
        # 'balance',
    }

    users = User.get(social={'$elemMatch': {
        'id': request.network,
        'user': data.user,
    }}, fields=fields)

    if len(users) > 1:
        await report.warning("More than 1 user", {
            'network': request.network,
            'social_user': data.user,
            'social_login': data.login,
        })

    elif len(users):
        new = False
        user = users[0]

        # Action tracking
        Track(
            title='acc_auth',
            data={
                'type': 'bot',
                'network': request.network,
            },
            user=user.id,
            token=request.token,
        ).save()

    # Register
    else:
        new = True
        user = await reg(request, data, 'bot')

    # Assignment of the token to the user

    if not request.token:
        raise ErrorAccess('auth')

    try:
        token = Token.get(ids=request.token, fields={'user'})
    except ErrorWrong:
        token = Token(id=request.token)

    if token.user and token.user != user.id:
        await report.warning("Reauth", {
            'from': token.user,
            'to': user.id,
            'token': request.token,
        })

    token.user = user.id
    token.save()

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }
