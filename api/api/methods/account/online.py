"""
The online socket of the account object of the API
"""

from ...funcs import check_params, online_start, report


async def handle(this, **x):
    """ Update online status """

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

    # # Visits

    # user_id = user_current['id'] if user_current else 0

    # db_condition = {
    #     'token': x['token'],
    #     'user': user_id,
    # }

    # utm = db.utms.find_one(db_condition)

    # if not utm:
    #     utm = {
    #         'token': x['token'],
    #         'user': user_id,
    #         # 'utm': utm_mark,
    #         'time': this.timestamp,
    #         'steps': [],
    #     }

    #     db.utms.insert_one(utm)

    # | Sessions (sid) |
    # | Tokens (token) |
    # | Users (id) |

    # Определить вкладку (tab - sid)
    # ? Проверка, что токен не скомпрометирован - по ip?

    # # UTM-метки

    # utm_mark = {}
    # params = x['url'].split('?')
    # if len(params) >= 2:
    #     params = dict(re.findall(r'([^=\&]*)=([^\&]*)', params[1]))
    #     if 'utm_source' in params and 'utm_medium' in params:
    #         utm_mark = {
    #             'source': params['utm_source'],
    #             'agent': params['utm_medium'],
    #         }

    # if utm:
    #     if utm_mark and not utm['utm']:
    #         utm['utm'] = utm_mark
    #         db.utms.save(utm)

    # else:
    #     utm = {
    #         'token': x['token'],
    #         'user': user_id,
    #         'utm': utm_mark,
    #         'time': this.timestamp,
    #         'steps': [],
    #     }

    #     db.utms.insert_one(utm)
