"""
The connect socket of the account object of the API
"""

from api.lib import report


async def handle(request, data):
    """ Connect """

    await report.debug('IN', request.socket)
