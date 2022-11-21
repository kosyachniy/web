"""
Reset online users process
"""

from models.socket import Socket
from routes.account.disconnect import online_stop


async def handle(sio):
    """ Reset online users """

    sockets = Socket.get(fields={})

    for socket in sockets:
        await online_stop(sio, socket.id)
