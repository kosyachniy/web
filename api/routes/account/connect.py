"""
The connect socket of the account object of the API
"""

from fastapi import APIRouter, Depends

from lib import report
from services.request import get_request


router = APIRouter()


@router.post("/connect/")
async def handler(request = Depends(get_request)):
    """ Connect """
    await report.debug('IN', request.socket)
