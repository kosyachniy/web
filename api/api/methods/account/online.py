"""
The online socket of the account object of the API
"""

from ...funcs import check_params, online_start, report


async def handle(this, **x):
    """ Update online status """

    # TODO: Проверка, что токен не скомпрометирован - по ip?
    # TODO: Определить вкладку (tab - sid)

    # Checking parameters
    check_params(x, (
        ('token', True, str),
    ))

    print('ON', this.sid)

    if not x['token']:
        report.warning("Invalid token", path='methods.account.online')
        return

    # Send sockets
    await online_start(this.sio, x['token'], this.sid)

    # TODO: UTM parameters
    # TODO: Promos

    # user_id = user_current['id'] if user_current else 0
    # utms = Mark.get(token=x['token'], user=user_id)

    # if utms:
    #     for utm in utms:
    #         utm.name = utm_mark
    #         utm.save()

    # else:
    #     utm = Mark(
    #         token=x['token'],
    #         user=user_id,
    #         name=utm_mark,
    #     )

    #     utm.save()
