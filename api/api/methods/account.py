"""
Account object of the API
"""

import re
import requests
import urllib
import json
import base64
import hashlib

from ..funcs import check_params, load_image, next_id, online_emit_add, \
                    other_sessions, online_user_update, online_emit_del, \
                    online_session_close, online_start
from ..funcs.mongodb import db
# from ..funcs.smsc import SMSC
from ..models.user import User, process_login, process_lower, \
                          pre_process_phone, process_password
from ..models.token import Token
from ..errors import ErrorBusy, ErrorInvalid, ErrorWrong, ErrorUpload, \
                     ErrorAccess


with open('keys.json', 'r') as file:
    keys = json.loads(file.read())
    VK = keys['vk']
    GOOGLE = keys['google']


async def auth(this, **x):
    """ Sign in / Sign up """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне

    # Checking parameters

    check_params(x, (
        ('login', True, str), # login / mail / phone
        ('password', True, str),
    ))

    # Data preparation

    # TODO: None / not ''
    # if 'password' in x and not x['password']:
    #     del x['password']

    fields = {
        'id',
        'login',
        'avatar',
        'name',
        'surname',
        'mail',
        'status',
    } # TODO: optimize

    # Login

    new = False

    try:
        login = process_login(x['login'])
        user = User.get(login=login, fields=fields)[0]
    except:
        new = True

    if new:
        try:
            mail = process_lower(x['mail'])
            user = User.get(mail=mail,fields=fields)[0]
        except:
            pass
        else:
            new = False

    if new:
        try:
            phone = pre_process_phone(x['phone'])
            user = User.get(phone=phone, fields=fields)[0]
        except:
            pass
        else:
            new = False

    if not new:
        password = process_password(x['password'])

        try:
            User.get(id=user.id, password=password)
        except:
            raise ErrorWrong('password')

    # Register

    if new:
        user_data = User(
            password=x['password'],
            mail=x['login'], # TODO: login / phone
            mail_verified=False,
        )
        user_data.save()
        user_id = user_data.id

        user = User.get(id=user_id, fields=fields)[0]

    # Assignment of the token to the user

    if not this.token:
        raise ErrorAccess('token')

    token = Token(
        id=this.token,
        user=user.id,
    )

    token.save()

    # Update online users

    await online_start(this.sio, this.timestamp, user, this.token)

    # Response

    res = user.json(fields={
        'id', 'login', 'avatar', 'name', 'surname', 'mail', 'status',
    })
    res['new'] = new

    return res # TODO: del None

# async def reg(this, **x):
#     """ Sign up """

#     # TODO: Сокет на авторизацию на всех вкладках токена
#     # TODO: Перезапись информации этого токена уже в онлайне

#     # Checking parameters

#     x = check_params(x, (
#         ('login', False, str),
#         ('password', False, str),
#         ('name', False, str),
#         ('surname', False, str),
#         ('avatar', False, str),
#         ('file', False, str),
#         ('mail', False, str),
#         ('social', False, list, dict),
#     ))

#     #

#     user = User(
#         login=x['login'],
#         password=x['password'],
#         avatar=x['avatar'],
#         name=x['name'],
#         surname=x['surname'],
#         mail=x['mail'],
#         mail_verified=False,
#         social=x['social'],
#     )

#     # Assignment of the token to the user

#     if not this.token:
#         raise ErrorAccess('token')

#     token = Token(
#         id=this.token,
#         user=user.id,
#     )

#     token.save()

#     # Update online users

#     await online_start(this.sio, this.timestamp, user, this.token)

#     # Response

#     res = {
#         'id': user.id,
#         'login': user.login,
#         'avatar': user.avatar,
#         'name': user.name,
#         'surname': user.surname,
#         'mail': user.mail,
#         'status': user.status,
#         'new': True,
#     }

#     return res

async def social(this, **x):
    """ By social network """

    # Checking parameters

    check_params(x, (
        ('user', True, int),
        # ('code', True, str),
    ))

    #

    # user_id = 0
    # new = False
    # mail = ''

    # # ВКонтакте
    # if x['id'] == 1:
    #     link = 'https://oauth.vk.com/access_token?client_id={}&client_secret=' \
    #            '{}&redirect_uri={}callback&code={}'
    #     response = json.loads(
    #         requests.get(
    #             link.format(
    #                 VK['client_id'],
    #                 VK['client_secret'],
    #                 this.client,
    #                 x['code'],
    #             )
    #         ).text
    #     )

    #     if 'user_id' in response:
    #         user_id = response['user_id']
    #     else:
    #         raise ErrorAccess('code')

    #     if 'email' in response:
    #         mail = response['email']

    # # Google
    # elif x['id'] == 3:
    #     link = 'https://accounts.google.com/o/oauth2/token'
    #     cont = {
    #         'client_id': GOOGLE['client_id'],
    #         'client_secret': GOOGLE['client_secret'],
    #         'redirect_uri': '{}callback'.format(this.client),
    #         'grant_type': 'authorization_code',
    #         'code': urllib.parse.unquote(x['code']),
    #     }
    #     response = json.loads(requests.post(link, json=cont).text)

    #     if 'access_token' not in response:
    #         raise ErrorAccess('code')

    #     link = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'
    #     response = json.loads(
    #         requests.get(
    #             link.format(response['access_token'])
    #         ).text
    #     )

    #     if 'id' in response:
    #         user_id = response['id']
    #     else:
    #         raise ErrorAccess('code')

    # # Wrong ID

    # if not user_id:
    #     raise ErrorWrong('id')

    # # Sign in

    # db_condition = {
    #     'social': {'$elemMatch': {'id': x['id'], 'user': user_id}},
    # }

    # db_filter = {
    #     '_id': False,
    #     'id': True,
    #     'login': True,
    #     'name': True,
    #     'surname': True,
    #     'avatar': True,
    #     'status': True,
    #     'mail': True,
    #     # 'rating': True,
    #     # 'balance': True,
    # }

    # res = db['users'].find_one(db_condition, db_filter)

    # # Wrong password
    # if not res:
    #     # Check keys

    #     name = ''
    #     surname = ''
    #     login = ''
    #     avatar = None

    #     if x['id'] == 1:
    #         if 'access_token' in response:
    #             token = response['access_token']
    #         else:
    #             raise ErrorAccess('code')

    #         # link = 'https://api.vk.com/method/account.getProfileInfo' \
    #         #        '?access_token={}&v=5.103'
    #         link = 'https://api.vk.com/method/users.get?user_ids={}&fields=' \
    #                'photo_max_orig,nickname&access_token={}&v=5.103'

    #         try:
    #             response = json.loads(
    #                 requests.get(
    #                     link.format(user_id, token)
    #                 ).text
    #             )['response'][0]
    #         except:
    #             raise ErrorAccess('vk')

    #         try:
    #             name = response['first_name']
    #             _check_name(name)
    #         except Exception:
    #             name = ''

    #         try:
    #             surname = response['last_name']
    #             _check_surname(surname)
    #         except Exception:
    #             surname = ''

    #         try:
    #             login = response['nickname']
    #             _check_login(login, this.user)
    #         except Exception:
    #             login = ''

    #         try:
    #             avatar = str(base64.b64encode(
    #                 requests.get(response['photo_max_orig']).content
    #             ))[2:-1]
    #         except Exception:
    #             avatar = None

    #         try:
    #             if mail:
    #                 _check_mail(mail, this.user)
    #         except Exception:
    #             mail = ''

    #     elif x['id'] == 3:
    #         # link = 'https://www.googleapis.com/oauth2/v1/userinfo' \
    #         #        '?access_token={}'.format(x['data']['access_token'])
    #         # res_google = json.loads(requests.get(link).text)

    #         try:
    #             name = response['given_name']
    #             _check_name(name)
    #         except Exception:
    #             name = ''

    #         try:
    #             surname = response['family_name']
    #             _check_surname(surname)
    #         except Exception:
    #             surname = ''

    #         try:
    #             mail = response['email']
    #             _check_mail(mail, this.user)
    #         except Exception:
    #             mail = ''

    #         try:
    #             if response['picture']:
    #                 avatar = str(base64.b64encode(
    #                     requests.get(response['picture']).content
    #                 ))[2:-1]
    #         except Exception:
    #             pass

    #     # Sign up

    #     db_condition = {
    #         'social': {'$elemMatch': {'user': user_id}},
    #     }

    #     db_filter = {
    #         '_id': True,
    #     }

    #     user = db['users'].find_one(db_condition, db_filter)

    #     if user:
    #         raise ErrorWrong('hash')

    #     # Sign up
    #     else:
    #         new = True

    #         user = _registrate(
    #             this.user,
    #             this.timestamp,
    #             social=[{
    #                 'id': x['id'],
    #                 'user': user_id,
    #             }],
    #             name=name,
    #             surname=surname,
    #             avatar=avatar,
    #             mail=mail,
    #         )

    #         #

    #         db_filter = {
    #             '_id': False,
    #             'id': True,
    #             'status': True,
    #             # 'balance': True,
    #             # 'rating': True,
    #             'login': True,
    #             'name': True,
    #             'surname': True,
    #             'mail': True,
    #         }

    #         user = db['users'].find_one({'id': user['id']}, db_filter)

    # # Assignment of the token to the user

    # if not this.token:
    #     raise ErrorInvalid('token')

    # req = {
    #     'token': this.token,
    #     'user': user['id'],
    #     'time': this.timestamp,
    # }
    # db['tokens'].insert_one(req)

    # # Update online users

    # await online_start(this.sio, this.timestamp, user, this.token)

    # # Response

    # res = {
    #     'id': user['id'],
    #     'login': user['login'],
    #     'name': user['name'],
    #     'surname': user['surname'],
    #     'status': user['status'],
    #     'mail': user['mail'],
    #     # 'balance': user['balance'],
    #     # 'rating': user['rating'],
    #     'new': new,
    # }

    # if 'avatar' in user:
    #     res['avatar'] = '/load/opt/' + user['avatar']
    # else:
    #     res['avatar'] = 'user.png'

    # return res

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

#     code = db['codes'].find_one({'phone': phone}, {'_id': True})

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

#     db['codes'].insert_one(req)

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

#         code = db['codes'].find_one(db_condition, db_filter)

#         if code:
#             # ! Входить по старым кодам
#             pass
#             # db['codes'].remove(code)

#         else:
#             raise ErrorWrong('code')

#     else:
#         code = {
#             'phone': x['phone'],
#         }

#         if 'promo' in x:
#             code['promo'] = x['promo']

#     #

#     user = db['users'].find_one({'phone': code['phone']})

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

#         user = db['users'].find_one({'id': res['id']})

#     if 'promo' in code:
#         # Referal code

#         if code['promo'].lower()[:5] == 'tensy':
#             referal_parent = int(re.sub('\D', '', code['promo']))

#             if user['id'] != referal_parent:
#                 user['referal_parent'] = referal_parent
#                 db['users'].save(user)

#         else:
#             # Bonus code

#             promo = db['promos'].find_one({'promo': code['promo'].upper()})

#             if not promo:
#                 promo = db['promos'].find_one({
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
#                             db['users'].save(user)

#                             # Сохранение результатов в промокоде

#                             promo['users'].append(user['id'])
#                             db['promos'].save(promo)

#     # Присвоение токена пользователю

#     req = {
#         'token': this.token,
#         'user': user['id'],
#         'time': this.timestamp,
#     }
#     db['tokens'].insert_one(req)

#     # Update online users

#     await online_start(this.sio, this.timestamp, user, this.token)

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

async def phone(this, **x):
    """ By phone """

    # Checking parameters

    check_params(x, (
        ('phone', True, str),
    ))

    #

    x['phone'] = _process_phone(x['phone'])

    # Login

    new = False

    if not list(db['users'].find({'phone': x['phone']}, {'_id': True})):
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

    res = db['users'].find_one(db_condition, db_filter)

    # Assignment of the token to the user

    if not this.token:
        raise ErrorAccess('token')

    req = {
        'token': this.token,
        'user': res['id'],
        'time': this.timestamp,
    }
    db['tokens'].insert_one(req)

    # Assignment of the tasks to the user

    for task in db['tasks'].find({'token': this.token}):
        task['user'] = res['id']
        del task['token']
        db['tasks'].save(task)

    # Update online users

    await online_start(this.sio, this.timestamp, res, this.token)

    # There is an active space

    db_condition = {
        '$or': [
            {'teacher': res['id']},
            {'student': res['id']}
        ],
        'status': {'$in': (0, 1)}
    }

    db_filter = {
        '_id': False,
        'id': True,
        'student': True,
        'task': True,
    }
    study = db['study'].find_one(db_condition, {'_id': False})

    if study:
        # Redirect to space

        space = '/space/{}/?task={}&type={}'.format(
            study['id'], study['task'],
            ('student', 'teacher')[study['student'] != res['id']],
        )

        sids = get_sids(res['id'])

        for sid in sids:
            this.sio.emit('space_return', {
                'url': space,
            }, room=sid, namespace='/main')

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

async def exit(this, **x):
    """ Log out """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне

    # Not authorized
    if not this.token:
        raise ErrorAccess('token')

    # Check token
    token = db['tokens'].find_one({'token': this.token}, {'_id': True})

    # Wrong token
    if not token:
        raise ErrorWrong('token')

    # Remove token
    db['tokens'].remove(token['_id']) # TODO: не удалять токены (выданные ботам)

    # Close session

    for online in db['online'].find({'token': this.token}):
        online_user_update(online)

        online['id'] = this.token
        online['status'] = 2

        if 'name' in online:
            del online['name']

        if 'surname' in online:
            del online['surname']

        if 'login' in online:
            del online['login']

        if 'avatar' in online:
            del online['avatar']

        online['start'] = this.timestamp

        db['online'].save(online)

        await online_emit_del(this.sio, this.user['id'])

    # ! Отправлять сокет всем сессиям этого браузера на выход

async def edit(this, **x):
    """ Edit personal information """

    # Checking parameters
    check_params(x, (
        ('name', False, str),
        ('surname', False, str),
        ('login', False, str),
        ('description', False, str),
        ('mail', False, str),
        ('password', False, str),
        ('avatar', False, str),
        ('file', False, str),
        ('social', False, list, dict),
    ))

    # No access
    if this.user['status'] < 3:
        raise ErrorAccess('edit')

    # Name
    if 'name' in x:
        _check_name(x['name'])
        this.user['name'] = x['name'].title()

    # Surname
    if 'surname' in x:
        _check_surname(x['surname'])
        this.user['surname'] = x['surname'].title()

    # Login
    if 'login' in x:
        x['login'] = x['login'].lower()

        if this.user['login'] != x['login']:
            _check_login(x['login'], this.user)
            this.user['login'] = x['login']

    # Mail
    if 'mail' in x:
        _check_mail(x['mail'], this.user)

    # Password
    if 'password' in x and len(x['password']):
        this.user['password'] = _process_password(x['password'])

    # Change fields
    for i in ('description', 'mail', 'social'):
        if i in x:
            this.user[i] = x[i]

    # Avatar
    if 'avatar' in x:
        try:
            file_type = x['file'].split('.')[-1]

        # Invalid file extension
        except:
            raise ErrorInvalid('file')

        try:
            link = load_image(x['avatar'], file_type)
            this.user['avatar'] = link

        # Error loading photo
        except:
            raise ErrorUpload('avatar')

    # Save changes
    db['users'].save(this.user)

    # Response

    res = dict()

    if 'avatar' in this.user:
        res['avatar'] = '/load/opt/' + this.user['avatar']
    else:
        res['avatar'] = 'user.png'

    return res

# # Recover password

# async def recover(this, **x):
#     # Checking parameters

#     check_params(x, (
#         ('login', True, str),
#     ))

#     # Get user

#     users = db['users'].find_one({'login': x['login']})

#     if not users:
#         raise ErrorWrong('login')

#     password = ''.join(random.sample(ALL_SYMBOLS, 15))
#     password_crypt = hashlib.md5(bytes(password, 'utf-8')).hexdigest()

#     # Send

#     # Update password

#     users['password'] = password_crypt
#     db['users'].save(users)

async def connect(this, **x):
    """ Connect """

    print('IN', this.sid)

async def online(this, **x):
    """ Online """

    print('ON', this.sid)

    # Define user

    db_filter = {
        '_id': False,
        'id': True,
    }

    user_current = db['tokens'].find_one({'token': x['token']}, db_filter)

    if user_current:
        db_filter = {
            '_id': False,
            'id': True,
            'login': True,
            'name': True,
            'surname': True,
            'avatar': True,
            'status': True,
        }

        user_current = db['users'].find_one({
            'id': user_current['id'],
        }, db_filter)

    # Online users
    ## Emit all users to this user

    # ? Отправлять неавторизованным пользователям информацию об онлайн?

    db_filter = {
        '_id': False,
        'sid': True,
        'id': True,
        'login': True,
        'name': True,
        'surname': True,
        'avatar': True,
        'status': True,
    }

    users_auth = list(db['online'].find({
        'login': {'$exists': True},
    }, db_filter))
    users_all = list(db['online'].find({}, db_filter))
    count = len({i['id'] for i in users_all})

    users_uniq = dict()
    # if user_current and user_current['status'] > 3: # Full info only for admins
    for i in users_auth:
        if i['id'] not in users_uniq:
            users_uniq[i['id']] = {
                'id': i['id'],
                'login': i['login'],
                'name': i['name'],
                'surname': i['surname'],
            }

            if 'avatar' in i:
                users_uniq[i['id']['avatar']] = '/load/opt/' + i['avatar']
            else:
                users_uniq[i['id']['avatar']] = 'user.png'

    if count:
        await this.sio.emit('online_add', {
            'count': count,
            'users': list(users_uniq.values()),
        }, room=this.sid)

    ## Already online

    user = User.get(ids=user_current['id']) if user_current else User()
    await online_start(this.sio, this.timestamp, user, x['token'], this.sid)

    # # Visits

    # user_id = user_current['id'] if user_current else 0

    # db_condition = {
    #     'token': x['token'],
    #     'user': user_id,
    # }

    # utm = db['utms'].find_one(db_condition)

    # if not utm:
    #     utm = {
    #         'token': x['token'],
    #         'user': user_id,
    #         # 'utm': utm_mark,
    #         'time': this.timestamp,
    #         'steps': [],
    #     }

    #     db['utms'].insert_one(utm)

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
    #         db['utms'].save(utm)

    # else:
    #     utm = {
    #         'token': x['token'],
    #         'user': user_id,
    #         'utm': utm_mark,
    #         'time': this.timestamp,
    #         'steps': [],
    #     }

    #     db['utms'].insert_one(utm)

async def disconnect(this, **x):
    """ Disconnect """

    print('OUT', this.sid)

    online = db['online'].find_one({'sid': this.sid})
    if not online:
        return

    # Close session

    online_user_update(online)
    online_session_close(online)
    await online_emit_del(this.sio, online['id'])
