"""
The connect socket of the account object of the API
"""

from fastapi import APIRouter, Depends

from services.request import get_request
from lib import report


router = APIRouter()


@router.post("/connect/")
async def handler(request = Depends(get_request)):
    """ Connect """
    await report.debug('IN', request.socket)
