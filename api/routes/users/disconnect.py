import time

from consys.errors import ErrorWrong

from lib import log
from lib.sockets import sio
from models.socket import Socket
from models.track import Track
from routes.users.online import _other_sessions, _online_count, get_user


async def online_stop(socket_id, close=True):
    """Stop online session of the user"""

    # TODO: Объединять сессии в онлайн по пользователю
    # TODO: Если сервер был остановлен, отслеживать сессию

    try:
        socket = Socket.get(socket_id)
    except ErrorWrong:
        # NOTE: method "exit" -> socket "disconnect"
        return

    user, _ = get_user(socket.token)

    # Update user online info
    now = time.time()
    if user.id:
        user.last_online = now
        user.save()

    # Action tracking
    Track(
        title="online",
        created=socket.created,
        expired=now,
        user=user.id,
        token=socket.token,
    ).save()

    # Remove token / Reset user
    if close:
        socket.rm()
    else:
        del socket.user
        socket.save()

    # Other sessions of this user
    other = _other_sessions(user.id, socket.token)
    if other:
        return

    # Send sockets about the user to all online users
    count = _online_count()
    if count:
        await sio.emit(
            "online_del",
            {
                "count": count,
                "users": [{"id": user.id}],  # TODO: Админам
            },
        )


@sio.on("disconnect")
async def disconnect(sid):
    """Disconnect"""
    log.debug("OUT", sid)
    await online_stop(sid)
