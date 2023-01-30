"""
The authorization via social networks method of the account object of the API
"""

from fastapi import APIRouter, Body, Request
from pydantic import BaseModel

from routes.account.auth import auth


router = APIRouter()


class Type(BaseModel):
    user: int
    login: str = None
    name: str = None
    surname: str = None
    image: str = None
    utm: str = None

@router.post("/bot/")
async def handler(
    request: Request,
    data: Type = Body(...),
):
    """ By bot """
    return await auth(request, data, 'bot', {
        'social': {
            '$elemMatch': {
                'id': request.state.network,
                'user': data.user,
            },
        },
    })
