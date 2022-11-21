"""
The cancel method of the payment object of the API
"""

from fastapi import APIRouter, Depends
from consys.errors import ErrorAccess, ErrorRepeat

from services.request import get_request


router = APIRouter()


@router.post("/cancel/")
async def handler(
    request = Depends(get_request),
):
    """ Delete payments data """

    # No access
    if request.user.status < 3:
        raise ErrorAccess('cancel')

    # No payment data
    if not request.user.pay:
        raise ErrorRepeat('cancel')

    del request.user.pay
    request.user.save()
