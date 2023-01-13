"""
The authorization via social networks method of the account object of the API
"""

from fastapi import APIRouter, Body, Request
from pydantic import BaseModel

from models.user import User
from models.track import Track
from routes.account.auth import reg, postauth
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
    request: Request,
    data: Type = Body(...),
):
    """ By bot """

    # TODO: image
    # TODO: the same token
    # TODO: block by token

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
        'id': request.state.network,
        'user': data.user,
    }}, fields=fields)

    if len(users) > 1:
        await report.warning("More than 1 user", {
            'network': request.state.network,
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
                'network': request.state.network,
            },
            user=user.id,
            token=request.state.token,
        ).save()

    # Register
    else:
        new = True
        user = await reg(
            request.state.network,
            request.state.ip,
            request.state.locale,
            request.state.token,
            data,
            'bot',
        )

    return postauth(request, user, new, fields)
