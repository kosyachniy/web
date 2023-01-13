"""
The blocking method of the user object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.user import User
from services.auth import sign


router = APIRouter()


class Type(BaseModel):
    id: int

@router.post("/block/")
async def handler(
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Block """

    # Get user
    subuser = User.get(data.id, fields={'status'})

    # No access
    if user.status < 6 or user.status > user.status:
        raise ErrorAccess('block')

    # Save
    subuser.status = 1
    subuser.save()

    # Response
    return {
        'status': subuser.status,
    }
