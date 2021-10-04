"""
The authorization by phone method of the account object of the API
"""

# import re

from consys.errors import ErrorAccess, ErrorInvalid

from ...lib import BaseType, validate, report
# from ...lib.sms import send_sms
from ...models.user import User, pre_process_phone
from ...models.token import Token
from ...models.action import Action
from .online import online_start


class Type(BaseType):
    phone: str
    # code: Union[str, int] = None
    # promo: str = None

@validate(Type)
async def handle(this, request, data):
    """ By phone """

    # TODO: the same token

    # No access
    if request.user.status < 2:
        raise ErrorAccess('phone')

    # Authorize

    fields = {
        'id',
        'login',
        'avatar',
        'name',
        'surname',
        'phone',
        'mail',
        'social',
        'status',
    }

    phone = pre_process_phone(data.phone)
    new = False
    users = User.get(phone=phone, fields=fields)

    if len(users) == 0:
        new = True
    elif len(users) > 1:
        await report.warning(
            "More than 1 user",
            {'phone': data.phone},
        )

    # Register
    if new:
        action = Action(
            name='account_reg',
            details={
                'network': request.network,
                'ip': request.ip,
                'phone': data.phone,
            },
        )

        try:
            user = User(
                phone=data.phone,
                phone_verified=False,
                actions=[action.json(default=False)],
            )
        except ValueError as e:
            raise ErrorInvalid(e) from e

        user.save()

        # Report
        await report.important(
            "User registration by phone",
            {
                'user': user.id,
                'phone': f"+{data.phone}",
                'token': request.token,
                'network': request.network,
            },
            tags=['reg'],
        )

    else:
        user = users[0]

        action = Action(
            name='account_auth',
            details={
                'ip': request.ip,
            },
        )

        user.actions.append(action.json(default=False))
        user.save()

    # Assignment of the token to the user

    if not request.token:
        raise ErrorAccess('phone')

    try:
        token = Token.get(ids=request.token, fields={'user'})
    except:
        token = Token(id=request.token)

    if token.user:
        await report.warning(
            "Reauth",
            {'from': token.user, 'to': user.id, 'token': request.token},
        )

    token.user = user.id
    token.save()

    # TODO: Pre-registration data (promos, actions, posts)

    # Update online users
    await online_start(this.sio, request.token)

    # TODO: redirect to active space
    # if space_id:
    #     for socket_id in Socket(user=user.id):
    #         this.sio.emit('space_return', {
    #             'url': f'/space/{space_id}',
    #         }, room=socket_id)

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }

# async def phone_send(this, request, data):
#     """ Send a code to the phone """

#     # Process a phone number

#     phone = _process_phone(data.phone)

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

#     promo = Promo(
#         phone=phone,
#         code=code,
#         token=request.token,
#         promo=data.promo,
#     )

#     promo.save()

#     #

#     res = await send_sms(
#         str(phone),
#         f"Hi!\n{code} — This is your login code."
#     )
#     await report.debug(phone, res)

#     # Response

#     res = {
#         'phone': phone,
#         'status': int(float(res[-1])) > 0,
#     }

#     return res

# async def phone_check(this, request):
#     """ Phone checking """

#     #

#     if not request.token:
#         raise ErrorInvalid('token')

#     #

#     data.phone = _process_phone(data.phone)

#     #

#     if data.code:
#         # Code preparation

#         data.code = str(data.code)

#         # Verification of code

#         db_condition = {
#             'code': data.code,
#         }

#         if data.phone:
#             db_condition['phone'] = data.phone
#         else:
#             db_condition['token'] = request.token

#         db_filter = {
#             '_id': False,
#             'phone': True,
#         }

#         code = db.codes.find_one(db_condition, db_filter)

#         if not code:
#             raise ErrorWrong('code')

#         # ! Входить по старым кодам
#         pass
#         # db.codes.remove(code)

#     else:
#         code = {
#             'phone': data.phone,
#         }

#         if data.promo:
#             code['promo'] = data.promo

#     #

#     user = db.users.find_one({'phone': code['phone']})

#     #

#     new = False

#     if not user:
#         res = _registrate(
#             request.user,
#             request.timestamp,
#             phone=code['phone'],
#         )

#         new = True

#         #

#         user = db.users.find_one({'id': res['id']})

#     if 'promo' in code:
#         # Referal code

#         if code['promo'].lower()[:5] == 'tensy':
#             referal_parent = int(re.sub(r'\D', '', code['promo']))

#             if user['id'] != referal_parent:
#                 db.users.update_one(
#                     {'id': user['id']},
#                     {'$set': {'referal_parent': referal_parent}}
#                 )

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
#                             db.users.update_one(
#                                 {'id': user['id']},
#                                 {'$inc': {'balance': promo['balance']}}
#                             )

#                             # Сохранение результатов в промокоде
#                             db.promos.update_one(
#                                 {'id': user['id']},
#                                 {'$push': {'users': user['id']}}
#                             )

#     # Присвоение токена пользователю

#     req = {
#         'token': request.token,
#         'user': user['id'],
#         'time': request.timestamp,
#     }
#     db.tokens.insert_one(req)

#     # Update online users

#     await online_start(this.sio, request.token)

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
