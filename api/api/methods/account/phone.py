"""
The authorization by phone method of the account object of the API
"""

# import re

from ...funcs import check_params, online_start, get_sids
from ...funcs.mongodb import db
# from ...funcs.smsc import SMSC
from ...errors import ErrorAccess # ErrorInvalid, ErrorWrong


async def handle(this, **x):
    """ By phone """

    # Checking parameters

    check_params(x, (
        ('phone', True, str),
    ))

    #

    x['phone'] = _process_phone(x['phone'])

    # Login

    new = False

    if not list(db.users.find({'phone': x['phone']}, {'_id': True})):
        # raise ErrorWrong('login')

        _registrate(
            this.user,
            this.timestamp,
            3 if this.language == 1 else 4,
            phone=x['phone'],
        )

        new = True

    #

    db_condition = {'phone': x['phone']}

    db_filter = {
        '_id': False,
        'id': True,
        'status': True,
        'balance': True,
        # 'rating': True,
        'login': True,
        'name': True,
        'surname': True,
        'busy': True,
        'avatar': True,
        'subscription': True,
        'channels': True,
        'description': True,
        'phone': True,
        'discount': True,
    }

    res = db.users.find_one(db_condition, db_filter)

    # Assignment of the token to the user

    if not this.token:
        raise ErrorAccess('token')

    req = {
        'token': this.token,
        'user': res['id'],
        'time': this.timestamp,
    }
    db.tokens.insert_one(req)

    # Assignment of the tasks to the user

    for task in db.tasks.find({'token': this.token}):
        task['user'] = res['id']
        del task['token']
        db.tasks.save(task)

    # Update online users

    await online_start(this.sio, this.token)

    # TODO: redirect to active space
    
    # if space_id:
    #     for sid in get_sids(user.id):
    #         this.sio.emit('space_return', {
    #             'url': f'/space/{space_id}',
    #         }, room=sid, namespace='/main')

    # Response

    req = {
        'id': res['id'],
        'status': res['status'],
        'balance': res['balance'],
        'login': res['login'],
        'new': new,
        'description': res['description'],
        'subscription': res['subscription'],
        'private': bool(len(res['channels'])),
        'phone': res['phone'] if 'phone' in res else '',
    }

    if 'avatar' in res:
        req['avatar'] = '/load/opt/' + res['avatar']
    else:
        req['avatar'] = 'user.png'

    if 'discount' in res:
        req['discount'] = res['discount']

    return req

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
