"""
Online status update functionality for the API
"""

import time

from ._reports import report
from .mongodb import db
from ..models.user import User
from ..models.token import Token
from ..models.socket import Socket


def _other_sessions(user_id, token=None):
    """ Checking for open online sessions of the user """

    if not user_id:
        if not token:
            return False

        sockets = Socket.get(token=token)

    else:
        sockets = Socket.get(user=user_id)

    return bool(sockets)

def _online_count():
    """ Counting the total number of online users """

    sockets = Socket.get(fields={'user', 'token'})
    count = len({el.user if el.user else el.token for el in sockets})

    return count


def get_user(token_id):
    """ Get user object by token """

    if token_id is not None:
        try:
            token = Token.get(ids=token_id, fields={'user'})

        except:
            token = Token(id=token_id)
            token.save()

        else:
            if token.user:
                return User.get(ids=token.user)

    return User()

def online_back(user_id):
    """ Checking how long has been online """

    online = db.sockets.find_one({'id': user_id}, {'_id': True})
    if online:
        return 0

    db_filter = {'_id': False, 'online.stop': True}
    user = db.users.find_one({'id': user_id}, db_filter)['online']

    last = max(i['stop'] for i in user)
    return time.time() - last

async def online_start(sio, token_id, socket_id=None):
    """ Start / update online session of the user """

    # TODO: save user data cache in db.sockets

    user = get_user(token_id)

    # Already online
    already = _other_sessions(user.id, token_id)

    # Save current socket with user & token data
    if socket_id:
        changed = False

        try:
            socket = Socket.get(ids=socket_id, fields={'user'})

        except:
            socket = Socket(
                id=socket_id,
                user=user.id,
                token=token_id,
            )
            changed = True

        else:
            if socket.token != token_id:
                socket.token = token_id
                changed = True
                report(
                    "Wrong `socket.token` in `funcs/_online/online_start`"
                , 1)

            if socket.user != user.id:
                socket.user = user.id
                changed = True
                report("Wrong `socket.user` in `funcs/_online/online_start`", 1)

        if changed:
            socket.save()

    # Update other sockets by token

    sockets = Socket.get(token=token_id, fields={'user'})

    for socket in sockets:
        socket.user = user.id
        socket.save()

    # Send sockets

    if already:
        return

    # TODO: Сокет на обновление сессий в браузере

    # Send sockets about the user to all online users

    count = _online_count()

    fields = {'id', 'login', 'avatar', 'name', 'surname'}
    data = user.json(fields=fields)
    # TODO: Full info for all / Full info only for admins

    res = {
        'count': count,
        'users': [data],
    }

    await sio.emit('online_add', res)

async def online_stop(sio, socket_id):
    """ Stop online session of the user """

    # TODO: Объединять сессии в онлайн по пользователю
    # TODO: Если сервер был остановлен, отслеживать сессию

    try:
        socket = Socket.get(ids=socket_id)
    except:
        report("Wrong `socket_id` in `funcs/_online/online_stop`", 1)
        return

    user = get_user(socket.token)

    # Update user online info

    if user.id:
        user.online.append({'start': socket.created, 'stop': time.time()})
        user.save()

    # Delete online session info

    socket = Socket.get(ids=socket_id)
    socket.rm()

    # Other sessions of this user

    other = _other_sessions(user.id, socket.token)

    if other:
        return

    # Send sockets about the user to all online users

    count = _online_count()

    await sio.emit('online_del', {
        'count': count,
        'users': [{'id': user.id}], # ! Админам
    })
