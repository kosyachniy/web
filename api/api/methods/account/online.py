"""
The online socket of the account object of the API
"""

from ...funcs import check_params, online_start, report


async def handle(this, **x):
    """ Online """

    # Checking parameters
    check_params(x, (
        ('token', True, str),
    ))

    print('ON', this.sid)

    if not x['token']:
        report("Invalid `token` in `methods/account/online`", 1)
        return

    # # Get token
    # try:
    #     token = Token.get(ids=x['token'], fields={'user'})
    # except:
    #     token = Token(id=x['token'])
    #     token.save()

    # # Get
    # user = User.get(ids=token.user, fields={
    #     'login',
    #     'avatar',
    #     'name',
    #     'surname',
    #     'status',
    # })

    # Online users

    # ## Emit all users to this user

    # # ? Отправлять неавторизованным пользователям информацию об онлайн?

    # db_filter = {
    #     '_id': False,
    #     'id': True,
    #     'user': True,
    # }

    # users_auth = list(db.sockets.find({
    #     'user': {'$ne': 0},
    # }, db_filter))
    # users_all = list(db.sockets.find({}, db_filter))
    # count = len({i['user'] for i in users_all})

    # sockets = Socket.get(fields={'user', 'token'})
    # count = len({el.user if el.user else el.token for el in sockets})

    # users_uniq = dict()
    # # if user_current and user_current['status'] > 3: # Full info only for admins
    # for i in users_auth:
    #     if i['user'] not in users_uniq:
    #         users_uniq[i['user']] = {
    #             'user': i['user'],
    #         }

    # if count:
    #     await this.sio.emit('online_add', {
    #         'count': count,
    #         'users': list(users_uniq.values()),
    #     }, room=this.sid)

    ## Already online

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
