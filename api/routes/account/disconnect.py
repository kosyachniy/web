"""
The disconnect socket of the account object of the API
"""

import time

from consys.errors import ErrorWrong

from models.socket import Socket
from models.track import Track
from routes.account.online import _other_sessions, _online_count, get_user
from lib import report
from app import sio


async def online_stop(socket_id, close=True):
    """ Stop online session of the user """

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
        title='online',
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
        await sio.emit('online_del', {
            'count': count,
            'users': [{'id': user.id}], # TODO: Админам
        })

@sio.on('disconnect')
async def disconnect(sid):
    """ Disconnect """
    await report.debug('OUT', sid)
    await online_stop(sid)
