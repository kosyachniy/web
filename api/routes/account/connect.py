"""
The connect socket of the account object of the API
"""

from app import sio
from lib import report


@sio.on('connect')
async def connect(sid, request, data):
    """ Connect """

    # TODO: ip = request['asgi.scope']['client'][0]

    await report.debug('IN', sid)
