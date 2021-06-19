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


def online_back(user_id):
    """ Checking how long has been online """

    online = db['sockets'].find_one({'id': user_id}, {'_id': True})
    if online:
        return 0

    db_filter = {'_id': False, 'online.stop': True}
    user = db['users'].find_one({'id': user_id}, db_filter)['online']

    last = max(i['stop'] for i in user)
    return time.time() - last

async def online_start(sio, token_id, socket_id=None):
    """ Start / update online session of the user """

    # TODO: save user data cache in db.sockets

    # Get user

    token = Token.get(ids=token_id)

    if token.user:
        user = User.get(ids=token.user)
    else:
        user = User()

    # Already online
    already = _other_sessions(user.id, token.id)

    # Save current socket with user & token data

    if socket_id:
        changed = False

        try:
            socket = Socket.get(ids=socket_id, fields={'user'})

        except:
            socket = Socket(
                id=socket_id,
                user=user.id,
                token=token.id,
            )
            changed = True

        else:
            if socket.token != token.id:
                socket.token = token.id
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

    sockets = Socket.get(token=token.id, fields={'user'})

    for socket in sockets:
        socket.user = user.id
        socket.save()

    # Send sockets

    if already:
        return

    # TODO: Сокет на обновление сессий в браузере

    # Send the socket about the user to all online users

    count = _online_count()

    fields = {'id', 'login', 'avatar', 'name', 'surname'}
    data = user.json(fields=fields)
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

    other = _other_sessions(user_id)

    if other:
        return

    ## Emit to clients

    sockets = Socket.get(fields={'user', 'token'})
    count = len({el.user if el.user else el.token for el in sockets})

    await sio.emit('online_del', {
        'count': count,
        'users': [{'id': user_id}], # ! Админам
    })
