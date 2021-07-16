"""
The online socket of the account object of the API
"""

from ...funcs import BaseType, validate, online_start, report


class Type(BaseType):
    token: str

@validate(Type)
async def handle(this, request):
    """ Update online status """

    # TODO: Проверка, что токен не скомпрометирован - по ip?
    # TODO: Определить вкладку (tab - sid)

    print('ON', this.socket)

    if not request.token:
        report.warning("Invalid token")
        return

    # Send sockets
    await online_start(this.sio, request.token, this.socket)

    # TODO: UTM parameters
    # TODO: Promos

    # user_id = user_current['id'] if user_current else 0
    # utms = Mark.get(token=request.token, user=user_id)

    # if utms:
    #     for utm in utms:
    #         utm.name = utm_mark
    #         utm.save()

    # else:
    #     utm = Mark(
    #         token=request.token,
    #         user=user_id,
    #         name=utm_mark,
    #     )

    #     utm.save()
