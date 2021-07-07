"""
The disconnect socket of the account object of the API
"""

from ...funcs import online_stop


# pylint: disable=unused-argument
async def handle(this, request):
    """ Disconnect """

    print('OUT', this.socket)

    await online_stop(this.sio, this.socket)
