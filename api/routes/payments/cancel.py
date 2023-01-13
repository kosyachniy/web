"""
The cancel method of the payment object of the API
"""

from fastapi import APIRouter, Depends
from consys.errors import ErrorAccess, ErrorRepeat

from services.auth import sign


router = APIRouter()


@router.post("/cancel/")
async def handler(
    user = Depends(sign),
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
