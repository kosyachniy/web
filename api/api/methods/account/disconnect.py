"""
The disconnect socket of the account object of the API
"""

from ...funcs import online_user_update, online_emit_del, online_session_close
from ...models.socket import Socket


async def handle(this, **x):
    """ Disconnect """

    print('OUT', this.sid)

    socket = Socket.get(ids=this.sid, fields={'user'}) # TODO: error handler
    if not socket:
        return

    # Close session

    online_user_update(socket.user)
    online_session_close(socket)
    await online_emit_del(this.sio, socket.user)
