"""
The disconnect socket of the account object of the API
"""

from ...funcs import online_stop
from ...models.socket import Socket


# pylint: disable=unused-argument
async def handle(this, **x):
    """ Disconnect """

    print('OUT', this.sid)

    await online_stop(this.sio, this.sid)
