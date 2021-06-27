"""
The logout method of the account object of the API
"""

from ...funcs import online_stop
from ...models.token import Token
from ...models.socket import Socket
from ...errors import ErrorAccess


# pylint: disable=unused-argument
async def handle(this, **x):
    """ Log out """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Отправлять сокет всем сессиям этого браузера на выход

    # Not authorized
    if this.user.status < 3:
        raise ErrorAccess('exit')

    # Check
    token = Token.get(ids=this.token, fields={})

    # Remove
    token.rm() # TODO: не удалять токены (выданные ботам)

    # Close session
    sockets = Socket.get(token=this.token, fields={})

    for socket in sockets:
        await online_stop(this.sio, socket.id)
