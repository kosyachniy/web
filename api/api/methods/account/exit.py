"""
The logout method of the account object of the API
"""

from ...funcs import online_user_update, online_emit_del
from ...funcs.mongodb import db
from ...models.socket import Socket
from ...errors import ErrorWrong, ErrorAccess


async def handle(this, **x):
    """ Log out """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне

    # Not authorized
    if not this.token:
        raise ErrorAccess('token')

    # Check token
    token = db['tokens'].find_one({'token': this.token}, {'_id': True})

    # Wrong token
    if not token:
        raise ErrorWrong('token')

    # Remove token
    db['tokens'].remove(token['_id']) # TODO: не удалять токены (выданные ботам)

    # Close session

    sockets = Socket.get(token=this.token)

    for socket in sockets:
        online_user_update(socket.user)

        socket.user = 0
        socket.created = this.timestamp
        socket.save()

        await online_emit_del(this.sio, this.user['id'])

    # ! Отправлять сокет всем сессиям этого браузера на выход