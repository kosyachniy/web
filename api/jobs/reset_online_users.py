from models.socket import Socket
from routes.users.disconnect import online_stop


async def handle(_):
    """Reset online users"""

    sockets = Socket.get(fields={})

    for socket in sockets:
        await online_stop(socket.id)
