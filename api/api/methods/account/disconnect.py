"""
The disconnect socket of the account object of the API
"""

from ...lib import online_stop, report


# pylint: disable=unused-argument
async def handle(this, request, data):
    """ Disconnect """

    await report.debug('OUT', request.socket)

    await online_stop(this.sio, request.socket)
