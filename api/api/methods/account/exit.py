"""
The logout method of the account object of the API
"""

from ...funcs import online_stop, report
from ...models.token import Token
from ...models.socket import Socket
from ...errors import ErrorAccess


# pylint: disable=unused-argument
async def handle(this, request):
    """ Log out """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Отправлять сокет всем сессиям этого браузера на выход

    # Not authorized
    if this.user.status < 3:
        report.error(
            "Wrong token",
            {'token': this.token, 'user': this.user.id},
        )

        raise ErrorAccess('exit')

    # Check
    token = Token.get(ids=this.token, fields={})

    # Remove
    # TODO: не удалять токены (выданные ботам)
    token.rm()

    # Close session

    sockets = Socket.get(token=this.token, fields={})

    for socket in sockets:
        await online_stop(this.sio, socket.id)
