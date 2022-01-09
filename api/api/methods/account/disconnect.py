"""
The disconnect socket of the account object of the API
"""

import time

from consys.errors import ErrorWrong

from api.lib import report
from api.models.job import Job
from api.models.socket import Socket
from api.models.track import Track
from api.methods.account.online import _other_sessions, _online_count, get_user


async def online_stop(sio, socket_id):
    """ Stop online session of the user """

    # TODO: Объединять сессии в онлайн по пользователю
    # TODO: Если сервер был остановлен, отслеживать сессию

    try:
        socket = Socket.get(ids=socket_id)
    except ErrorWrong:
        # NOTE: method "exit" -> socket "disconnect"
        return

    user = get_user(socket.token)

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
        user=user.id or socket.token,
    ).save()

    # Delete online session info
    socket = Socket.get(ids=socket_id)
    socket.rm()

    # Other sessions of this user

    other = _other_sessions(user.id, socket.token)

    if other:
        return

    # Send sockets about the user to all online users

    count = _online_count()

    if count:
        Job(
            method='online_del',
            data={
                'count': count,
                'users': [{'id': user.id}], # TODO: Админам
            },
        ).save()
        # await sio.emit('online_del', {
        #     'count': count,
        #     'users': [{'id': user.id}], # TODO: Админам
        # })


async def handle(request, data):
    """ Disconnect """

    await report.debug('OUT', request.socket)

    await online_stop(request.sio, request.socket)
