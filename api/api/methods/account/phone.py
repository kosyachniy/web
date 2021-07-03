"""
The authorization by phone method of the account object of the API
"""

# import re

from ...funcs import check_params, online_start, report
from ...models.user import User, pre_process_phone
from ...models.token import Token
# from ...funcs.smsc import SMSC
from ...errors import ErrorAccess


async def handle(this, **x):
    """ By phone """

    # Checking parameters
    check_params(x, (
        ('phone', True, str),
    ))

    # Authorize

    fields = {
        'login',
        'avatar',
        'name',
        'surname',
        'mail',
        'status',
    }

    phone = pre_process_phone(x['phone'])
    new = False
    users = User.get(phone=phone, fields=fields)

    if len(users) == 0:
        new = True
    elif len(users) > 1:
        report.warning(
            "More than 1 user",
            {'phone': x['phone']},
            path='methods.account.phone'
        )

    # Register
    if new:
        user_data = User(
            phone=x['phone'],
            phone_verified=False,
        )
        user_data.save()
        user_id = user_data.id

        user = User.get(ids=user_id, fields=fields)

    else:
        user = users[0]

    # Assignment of the token to the user

    if not this.token:
        raise ErrorAccess('phone')

    if new and this.user.status > 2:
        token = Token.get(ids=this.token, fields={'user'})

        report.warning(
            "Reauth",
            {'from': token.user, 'to': user.id},
            path='methods.account.phone'
        )

        token.user = user.id

    else:
        token = Token(
            id=this.token,
            user=user.id,
        )

    token.save()

    # # TODO: Assignment of the tasks to the user
    # for task in db.tasks.find({'token': this.token}):
    #     task['user'] = res['id']
    #     del task['token']
    #     db.tasks.save(task)

    # Update online users
    await online_start(this.sio, this.token)

    # # TODO: redirect to active space
    # if space_id:
    #     for socket_id in Socket(user=user.id):
    #         this.sio.emit('space_return', {
    #             'url': f'/space/{space_id}',
    #         }, room=socket_id)

    # Response
    return {
        **user.json(fields={
            'id',
            'login',
            'avatar',
            'name',
            'surname',
            'mail',
            'status',
        }),
        'new': new,
    }

# By phone

# async def phone_send(this, **x):
#     """ Send a code to the phone """

#     # Checking parameters

#     check_params(x, (
#         ('phone', True, str),
#         ('promo', False, str),
#     ))

#     # Process a phone number

#     phone = _process_phone(x['phone'])

#     # Already sent

#     code = db.codes.find_one({'phone': phone}, {'_id': True})

#     if code:
#         raise ErrorRepeat('send')

#     # Code generation

#     ALL_SYMBOLS = string.digits
#     generate = lambda length=4: ''.join(
#         random.choice(ALL_SYMBOLS) for _ in range(length)
#     )
#     code = generate()

#     #

#     req = {
#         'phone': phone,
#         'code': code,
#         'token': this.token,
#         'time': this.timestamp,
#     }

#     if 'promo' in x:
#         req['promo'] = x['promo']

#     db.codes.insert_one(req)

#     #

#     sms = SMSC()
#     res = sms.send_sms(
#         str(phone),
#         'Hi!\n{} — This is your login code.'.format(code)
#     )
#     print(phone, res)

#     # Response

#     res = {
#         'phone': phone,
#         'status': int(float(res[-1])) > 0,
#     }

#     return res

# async def phone_check(this, **x):
#     """ Phone checking """

#     # Checking parameters

#     check_params(x, (
#         ('phone', False, str),
#         ('code', False, (int, str)),
#         ('promo', False, str),
#     ))

#     #

#     if not this.token:
#         raise ErrorInvalid('token')

#     #

#     if 'code' in x and not x['code']:
#         del x['code']

#     if 'phone' in x:
#         x['phone'] = _process_phone(x['phone'])

#     #

#     if 'code' in x:
#         # Code preparation

#         x['code'] = str(x['code'])

#         # Verification of code

#         db_condition = {
#             'code': x['code'],
#         }

#         if 'phone' in x:
#             db_condition['phone'] = x['phone']
#         else:
#             db_condition['token'] = this.token

#         db_filter = {
#             '_id': False,
#             'phone': True,
#         }

#         code = db.codes.find_one(db_condition, db_filter)

#         if code:
#             # ! Входить по старым кодам
#             pass
#             # db.codes.remove(code)

#         else:
#             raise ErrorWrong('code')

#     else:
#         code = {
#             'phone': x['phone'],
#         }

#         if 'promo' in x:
#             code['promo'] = x['promo']

#     #

#     user = db.users.find_one({'phone': code['phone']})

#     #

#     new = False

#     if not user:
#         res = _registrate(
#             this.user,
#             this.timestamp,
#             phone=code['phone'],
#         )

#         new = True

#         #

#         user = db.users.find_one({'id': res['id']})

#     if 'promo' in code:
#         # Referal code

#         if code['promo'].lower()[:5] == 'tensy':
#             referal_parent = int(re.sub('\D', '', code['promo']))

#             if user['id'] != referal_parent:
#                 user['referal_parent'] = referal_parent
#                 db.users.save(user)

#         else:
#             # Bonus code

#             promo = db.promos.find_one({'promo': code['promo'].upper()})

#             if not promo:
#                 promo = db.promos.find_one({
#                     'promo': code['promo'].lower(),
#                 })

#                 if promo:
#                     # Нет доступа

#                     if user['status'] >= promo['admin']:
#                         # Повтор

#                         if promo['repeat'] \
#                             or user['id'] not in promo['users']:
#                             # Выполнение скрипта

#                             user['balance'] += promo['balance']
#                             db.users.save(user)

#                             # Сохранение результатов в промокоде

#                             promo['users'].append(user['id'])
#                             db.promos.save(promo)

#     # Присвоение токена пользователю

#     req = {
#         'token': this.token,
#         'user': user['id'],
#         'time': this.timestamp,
#     }
#     db.tokens.insert_one(req)

#     # Update online users

#     await online_start(this.sio, this.token)

#     # Response

#     res = {
#         'id': user['id'],
#         'login': user['login'],
#         'name': user['name'],
#         'surname': user['surname'],
#         'avatar': '/load/opt/' + user['avatar'],
#         'status': user['status'],
#         'mail': user['mail'],
#         # 'balance': user['balance'],
#         # 'rating': user['rating'],
#         'new': new,
#     }

#     return res
