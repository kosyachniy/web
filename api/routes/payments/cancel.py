"""
The cancel method of the payment object of the API
"""

from fastapi import APIRouter, Depends
from consys.errors import ErrorAccess, ErrorRepeat

from services.auth import auth


router = APIRouter()


@router.post("/cancel/")
async def handler(
    user = Depends(auth),
):
    """ Delete payments data """

    # No access
    if user.status < 3:
        raise ErrorAccess('cancel')

    # No payment data
    if not user.pay:
        raise ErrorRepeat('cancel')

    del user.pay
    user.save()
