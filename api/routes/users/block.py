"""
The blocking method of the user object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.user import User
from services.request import get_request


router = APIRouter()


class Type(BaseModel):
    id: int

@router.post("/block/")
async def handler(
    data: Type = Body(...),
    request = Depends(get_request),
):
    """ Block """

    # Get user
    user = User.get(ids=data.id, fields={'status'})

    # No access
    if request.user.status < 6 or user.status > request.user.status:
        raise ErrorAccess('block')

    # Save
    user.status = 1
    user.save()

    # Response
    return {
        'status': user.status,
    }
