"""
The main functionality for the API
"""

import os
import re
import time
import base64
import string
import random
import json

import requests
from PIL import Image, ExifTags

from ._codes import NETWORKS, LANGUAGES
from .mongodb import db
from .tg_bot import send as send_tg
from ..models.socket import Socket
from ..errors import ErrorSpecified, ErrorInvalid, ErrorType


# pylint: disable=W0621
with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    SIDE_OPTIMIZED = sets['side_optimized']
    MODE = sets['mode']
    BUG_CHAT = sets['bug_chat']

ALL_SYMBOLS = string.digits + string.ascii_letters


# Funcs

def generate(length: int = 32) -> str:
    """ Token / code generation """

    return ''.join(random.choice(ALL_SYMBOLS) for _ in range(length))

def get_file(url, num):
    """ Check existence the file by name """

    for i in os.listdir('../data/load/{}/'.format(url)):
        if re.search(rf"^{str(num)}.", i):
            return i

    return None

def max_image(url):
    """ Next image ID """

    files = os.listdir(url)
    k = 0
    for i in files:
        j = re.findall(r'\d+', i)
        if len(j) and int(j[0]) > k:
            k = int(j[0])
    return k+1

def load_image(data, encoding='base64', file_format=None):
    """ Upload image """

    url = '../data/load/'
    url_opt = url + 'opt/'

    if encoding == 'base64':
        file_format = re.search(r'data:image/.+;base64,', data).group()[11:-8]
        b64 = data.split(',')[1]
        data = base64.b64decode(b64)

    file_id = max_image(url)
    file_id = '{}{}{}'.format(
        '0' * max(0, 10-len(str(file_id))),
        file_id,
        ''.join(random.choice(string.ascii_lowercase) for _ in range(6)),
    )
    file_format = file_format.lower()
    file_name = '{}.{}'.format(file_id, file_format)
    url += file_name
    url_opt += file_name

    with open(url, 'wb') as file:
        file.write(data)

    # EXIF data

    try:
        img = Image.open(url)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = dict(img._getexif().items())

        if exif[orientation] == 3:
            img = img.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            img = img.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            img = img.transpose(Image.ROTATE_90)

        img.save(url)
        img.close()

    except (AttributeError, KeyError, IndexError):
        pass

    # Optimized version

    img = Image.open(url)

    if img.size[0] > img.size[1]:
        hpercent = (SIDE_OPTIMIZED / float(img.size[1]))
        wsize = int(float(img.size[0]) * float(hpercent))
        img = img.resize((wsize, SIDE_OPTIMIZED), Image.ANTIALIAS)
    else:
        wpercent = (SIDE_OPTIMIZED / float(img.size[0]))
        hsize = int(float(img.size[1]) * float(wpercent))
        img = img.resize((SIDE_OPTIMIZED, hsize), Image.ANTIALIAS)

    img.save(url_opt)

    # Response

    return file_name

# pylint: disable=W0702
def reimg(text):
    """ Replace image in text """

    # TODO: Переписать

    k = 0

    while True:
        img = re.search(r'<img ', text[k:])
        if img:
            first, last = list(img.span())
            last = first + text[k+first:].index('>')
            result = ''
            if 'src=' in text[k+first:k+last]:
                if re.search(
                    r'image/.*;',
                    text[k+first:k+last]
                ) and 'base64,' in text[k+first:k+last]:
                    start = k + first + text[k+first:].index('base64,') + 7
                    try:
                        stop = start + text[start:].index('"')
                    except:
                        stop = start + text[start:].index('\'')

                    b64 = text[start:stop]
                    form = re.search(
                        r'image/.*;',
                        text[k+first:start]
                    ).group(0)[6:-1]
                    adr = load_image(b64, form)

                    # result = '<img src="/load/{}">'.format(adr)
                    result = '<img src="/load/opt/{}">'.format(adr)
                else:
                    start = k + re.search(r'src=.*', text[k:]).span()[0] + 5
                    try:
                        stop = start + text[start:].index('"')
                    except:
                        stop = start + text[start:].index('\'')

                    href = text[start:stop]

                    if href[:4] == 'http':
                        b64 = str(base64.b64encode(
                            requests.get(href).content
                        ))[2:-1]
                        form = href.split('.')[-1]
                        if 'latex' in form or '/' in form or len(form) > 5:
                            form = 'png'
                        adr = load_image(b64, form)

                        # result = '<img src="/load/{}">'.format(adr)
                        result = '<img src="/load/opt/{}">'.format(adr)

            if result:
                text = text[:k+first] + result + text[k+last+1:]
                k += first + len(result)
            else:
                k += last
        else:
            break

    return text

def get_user(user_id):
    """ Get user by ID """

    if user_id:
        db_condition = {
            'id': user_id,
        }

        db_filter = {
            '_id': False,
            'id': True,
            'login': True,
            'name': True,
            'surname': True,
            'avatar': True,
        }

        user_req = db['users'].find_one(db_condition, db_filter)

        if 'avatar' in user_req:
            user_req['avatar'] = '/load/opt/' + user_req['avatar']
        else:
            user_req['avatar'] = 'user.png'

    else:
        user_req = 0

    return user_req

def check_params(data, filters):
    """ Checking parameters """

    # TODO: Удалять другие поля (которых нет в списке)

    for i in filters:
        if i[0] in data:
            # Invalid data type
            if not isinstance(i[2], (list, tuple)):
                el_type = (i[2],)
            else:
                el_type = i[2]

            cond_type = not isinstance(data[i[0]], el_type)
            cond_iter = isinstance(data[i[0]], (tuple, list))

            try:
                cond_iter_el = cond_iter \
                    and any(not isinstance(j, i[3]) for j in data[i[0]])
            except:
                raise ErrorType(i[0])

            if cond_type or cond_iter_el:
                raise ErrorType(i[0])

            cond_null = isinstance(i[-1], bool) and i[-1] and cond_iter \
                and not data[i[0]]

            if cond_null:
                raise ErrorInvalid(i[0])

        # Not all fields are filled
        elif i[1]:
            raise ErrorSpecified(i[0])

        # Default
        else:
            data[i[0]] = None

    return data

def next_id(name):
    """ Next DB ID """

    id_last = list(db[name].find({}, {'id': True, '_id': False}).sort('id', -1))

    if id_last:
        return id_last[0]['id'] + 1

    return 1

# Codes

def get_network(code):
    """ Get network code by cipher """

    if code in NETWORKS:
        return NETWORKS.index(code)

    if code in range(len(NETWORKS)):
        return code

    return 0

def get_language(code):
    """ Get language code by cipher """

    if code in LANGUAGES:
        return LANGUAGES.index(code)

    if code in range(len(LANGUAGES)):
        return code

    return 0

def get_user_by_token(token):
    """ Get user object by token """

    from ..models.user import User

    user = User()

    if not token:
        return user

    db_filter = {'user': True, '_id': False}
    token_data = db['tokens'].find_one({'token': token}, db_filter)

    if not token_data or not token_data['user']:
        return user

    try:
        user = User.get(ids=token_data['user'])
    except:
        pass

    return user

def get_status(user):
    """ Get available status for the user """

    if user['status'] >= 6:
        return 0

    if user['status'] >= 5:
        return 1

    if user['status'] >= 3:
        return 3

    return 3 # !

def get_status_condition(user):
    """ Get conditions for database by user """

    if user['id']:
        return {
            '$or': [{
                'status': {'$gte': get_status(user)},
            }, {
                'user': user['id'],
            }]
        }

    return {
        'status': {'$gte': get_status(user)},
    }

def get_id(sid):
    """ Get user ID by sid """

    db_filter = {
        '_id': False,
        'id': True,
    }

    user = db['sockets'].find_one({'sid': sid}, db_filter)

    if not user:
        raise Exception('sid not found')

    # ?
    if not isinstance(user['id'], int) or not user['id']:
        return 0

    return user['id']

def get_sids(user):
    """ Get all sids of user by ID """

    db_filter = {
        '_id': False,
        'sid': True,
    }

    user_sessions = db['sockets'].find({'id': user}, db_filter)

    return [i['sid'] for i in user_sessions]

def get_date(text, template='%Y%m%d'):
    """ Get date from timestamp """

    return time.strftime(template, time.localtime(text))

def reduce_params(cont, params):
    """ Leave only the required fields for objects in the list """

    def only_params(element):
        return {i: element[i] for i in params}

    return list(map(only_params, cont))

def online_back(user_id):
    """ Checking how long has been online """

    online = db['sockets'].find_one({'id': user_id}, {'_id': True})
    if online:
        return 0

    db_filter = {'_id': False, 'online.stop': True}
    user = db['users'].find_one({'id': user_id}, db_filter)['online']

    last = max(i['stop'] for i in user)
    return time.time() - last

def other_sessions(user_id, token=None):
    """ Checking for open online sessions of the user """

    if not user_id:
        if not token:
            return False

        sockets = Socket.get(token=token)

    else:
        sockets = Socket.get(user=user_id)

    return bool(sockets)

# Online update

async def online_start(sio, timestamp, user, token, sid=None):
    """ Start / update online session of the user """

    # TODO: save user data cache in db.online

    # Already online
    already = other_sessions(user.id, token)

    # Update DB

    sockets = Socket.get(token=token, fields={'user'})

    for socket in sockets:
        socket.user = user.id
        socket.save()

    if not sockets:
        socket = Socket(
            id=sid, # TODO: если нет sid нужно добавить уникальный, т.к. иначе будет создавать при сохранении новый экземпляр
            user=user.id,
            token=token,
        )

        socket.save()

    # Send sockets
    if not already:
        await online_emit_add(sio, user)

    # TODO: Сокет на обновление сессий в браузере

async def online_emit_add(sio, user):
    """ Send sockets about adding / updating online users """

    # Counting the total number of online users

    sockets = Socket.get(fields={'user', 'token'})
    count = len({el.user if el.user else el.token for el in sockets})

    # Send a socket about the user to all online users

    fields = {'id', 'login', 'avatar', 'name', 'surname'}
    data = user.json(fields=fields) if user else {} # TODO: delete if-else
    # TODO: Full info for all / Full info only for admins

    res = {
        'count': count,
        'users': [data],
    }

    await sio.emit('online_add', res)

def online_user_update(user_id):
    """ User data about online update """

    # TODO: Объединять сессии в онлайн по пользователю
    # TODO: Если сервер был остановлен, отслеживать сессию

    if not user_id:
        return

    user = User.get(ids=user_id) # TODO: error handler
    user.online.append({'start': online['start'], 'stop': time.time()})
    user.save()

def online_session_close(socket):
    """ Close online session """

    # Remove from online users

    socket = db['sockets'].find_one({'id': socket.id})
    db['sockets'].remove(socket)

async def online_emit_del(sio, user_id):
    """ Send sockets about deleting online users """

    if not user_id:
        return

    # Online users
    ## Other sessions of this user

    other = other_sessions(user_id)

    if other:
        return

    ## Emit to clients

    db_filter = {
        '_id': False,
        'id': True,
    }

    sockets = Socket.get(fields={'user', 'token'})
    count = len({el.user if el.user else el.token for el in sockets})

    await sio.emit('online_del', {
        'count': count,
        'users': [{'id': user_id}], # ! Админам
    })

# Report

SYMBOLS = ['🟢', '🟡', '🔴', '❗️', '✅']
TYPES = ['INFO', 'WARNING', 'ERROR', 'CRITICAL', 'IMPORTANT']

def report(text, type_=0, additional=''):
    """ Report logs and notifications on Telegram chat or in log files """

    if MODE != "PROD" and type_ == 0:
        return

    preview = f"{SYMBOLS[type_]} {MODE} {TYPES[type_]}\n---------------\n"
    text = preview + text
    if additional:
        text_with_additional = text + '\n\n' + str(additional)
    else:
        text_with_additional = text

    try:
        send_tg(BUG_CHAT, text_with_additional, markup=None)
    except Exception as error:
        if additional:
            print("❗️❗️❗️", error)
            print(additional)

            try:
                send_tg(BUG_CHAT, text, markup=None)
            except Exception as error:
                print("❗️❗️❗️", error)
                print(type_, text)

        else:
            print("❗️❗️❗️", error)
            print(type_, text)
