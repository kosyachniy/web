"""
The logout method of the account object of the API
"""

from fastapi import APIRouter # Request, Depends
# from consys.errors import ErrorAccess

# from models.token import Token
# from models.socket import Socket
# from services.auth import sign
# from routes.account.disconnect import online_stop
# from lib import report


router = APIRouter()


@router.post("/exit/")
async def handler(
    # request: Request,
    # user = Depends(sign),
):
    """ Log out """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Отправлять сокет всем сессиям этого браузера на выход

    # # Not authorized
    # if user.status < 3:
    #     await report.error("Wrong token", {
    #         'token': request.state.token,
    #         'user': user.id,
    #     })

    #     raise ErrorAccess('exit')

    # # Check
    # token = Token.get(request.state.token, fields={})

    # # Remove
    # # TODO: не удалять токены (выданные ботам)
    # token.rm()

    # # Close session

    # sockets = Socket.get(token=request.state.token, fields={})

    # for socket in sockets:
    #     await online_stop(socket.id)
