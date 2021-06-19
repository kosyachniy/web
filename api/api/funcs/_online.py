"""
Online status update functionality for the API
"""

import time

from .mongodb import db
from ..models.user import User
from ..models.socket import Socket


def online_back(user_id):
    """ Checking how long has been online """

    online = db['sockets'].find_one({'id': user_id}, {'_id': True})
    if online:
        return 0

    db_filter = {'_id': False, 'online.stop': True}
    user = db['users'].find_one({'id': user_id}, db_filter)['online']

    last = max(i['stop'] for i in user)
    return time.time() - last

def other_sessions(user_id, token=None):
    """ Checking for open online sessions of the user """

    if not user_id:
        if not token:
            return False

        sockets = Socket.get(token=token)

    else:
        sockets = Socket.get(user=user_id)

    return bool(sockets)

# Online update

async def online_start(sio, user, token, sid=None):
    """ Start / update online session of the user """

    # TODO: save user data cache in db.online

    # Already online
    already = other_sessions(user.id, token)

    # Update DB

    sockets = Socket.get(token=token, fields={'user'})

    for socket in sockets:
        socket.user = user.id
        socket.save()

    if not sockets:
        # TODO: если нет sid нужно добавить уникальный, т.к. иначе будет
        # создавать при сохранении новый экземпляр
        socket = Socket(
            id=sid,
            user=user.id,
            token=token,
        )

        socket.save()

    # Send sockets
    if not already:
        await online_emit_add(sio, user)

    # TODO: Сокет на обновление сессий в браузере

async def online_emit_add(sio, user):
    """ Send sockets about adding / updating online users """

    # Counting the total number of online users

    sockets = Socket.get(fields={'user', 'token'})
    count = len({el.user if el.user else el.token for el in sockets})

    # Send a socket about the user to all online users

    fields = {'id', 'login', 'avatar', 'name', 'surname'}
    data = user.json(fields=fields) if user else {} # TODO: delete if-else
    # TODO: Full info for all / Full info only for admins

    res = {
        'count': count,
        'users': [data],
    }

    await sio.emit('online_add', res)

def online_user_update(user_id):
    """ User data about online update """

    # TODO: Объединять сессии в онлайн по пользователю
    # TODO: Если сервер был остановлен, отслеживать сессию

    if not user_id:
        return

    user = User.get(ids=user_id) # TODO: error handler
    user.online.append({'start': online['start'], 'stop': time.time()})
    user.save()

def online_session_close(socket):
    """ Close online session """

    # Remove from online users

    socket = db['sockets'].find_one({'id': socket.id})
    db['sockets'].remove(socket)

async def online_emit_del(sio, user_id):
    """ Send sockets about deleting online users """

    if not user_id:
        return

    # Online users
    ## Other sessions of this user

    other = other_sessions(user_id)

    if other:
        return

    ## Emit to clients

    sockets = Socket.get(fields={'user', 'token'})
    count = len({el.user if el.user else el.token for el in sockets})

    await sio.emit('online_del', {
        'count': count,
        'users': [{'id': user_id}], # ! Админам
    })
