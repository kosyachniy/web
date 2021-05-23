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

from .mongodb import db
from .tg_bot import send as send_tg
from ..errors import ErrorSpecified, ErrorInvalid, ErrorType


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    SIDE_OPTIMIZED = sets['side_optimized']
    MODE = sets['mode']
    BUG_CHAT = sets['bug_chat']


# Funcs

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

def load_image(
    data, file_type=None, file_coding='base64', file_url='', file_id=None,
):
    """ Upload image """

    url = '../data/load/' + file_url
    url_opt = url + 'opt/'

    if file_coding == 'base64':
        data = base64.b64decode(data)

    if file_type == '' or file_type is None:
        file_type = 'jpg'

    file_type = file_type.lower()

    if file_id:
        for i in os.listdir(url):
            if re.search(r'^{}\.'.format(file_id), i):
                os.remove('{}/{}'.format(url, i))

        for i in os.listdir(url_opt):
            if re.search(r'^{}\.'.format(file_id), i):
                os.remove('{}/{}'.format(url_opt, i))

    else:
        file_id = max_image(url)
        file_id = '{}{}{}'.format(
            '0' * max(0, 10-len(str(file_id))),
            file_id,
            ''.join(random.choice(string.ascii_lowercase) for _ in range(10)),
        )

    file_name = '{}.{}'.format(file_id, file_type)
    url += file_name
    url_opt += file_name

    with open(url, 'wb') as file:
        file.write(data)

    # EXIF data

    try:
        img = Image.open(url)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
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

    if file_url:
        return '{}/{}'.format(file_url, file_name)

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
            if type(i[2]) not in (list, tuple):
                el_type = (i[2],)
            else:
                el_type = i[2]

            cond_type = type(data[i[0]]) not in el_type
            cond_iter = type(data[i[0]]) in (tuple, list)

            try:
                cond_iter_el = cond_iter \
                    and any(type(j) != i[3] for j in data[i[0]])
            except:
                raise ErrorType(i[0])

            if cond_type or cond_iter_el:
                raise ErrorType(i[0])

            cond_null = type(i[-1]) == bool and i[-1] and cond_iter \
                and not data[i[0]]

            if cond_null:
                raise ErrorInvalid(i[0])

        # Not all fields are filled
        elif i[1]:
            raise ErrorSpecified(i[0])

def next_id(name):
    """ Next DB ID """

    id_last = list(db[name].find({}, {'id': True, '_id': False}).sort('id', -1))

    if id_last:
        return id_last[0]['id'] + 1

    return 1

def get_language(name):
    """ Convert language to code """

    languages = ('en', 'ru', 'fi', 'es')

    if name in languages:
        name = languages.index(name)

    elif name not in range(len(languages)):
        name = 0

    return name

def get_status(user):
    """ Get available status for the user """

    if user['admin'] >= 6:
        return 0

    if user['admin'] >= 5:
        return 1

    if user['admin'] >= 3:
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

    user = db['online'].find_one({'sid': sid}, db_filter)

    if not user:
        raise Exception('sid not found')

    # ?
    if type(user['id']) != int or not user['id']:
        return 0

    return user['id']

def get_sids(user):
    """ Get all sids of user by ID """

    db_filter = {
        '_id': False,
        'sid': True,
    }

    user_sessions = db['online'].find({'id': user}, db_filter)

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

    online = db['online'].find_one({'id': user_id}, {'_id': True})
    if online:
        return 0

    db_filter = {'_id': False, 'online.stop': True}
    user = db['users'].find_one({'id': user_id}, db_filter)['online']

    last = max(i['stop'] for i in user)
    return time.time() - last

def other_sessions(user_id):
    """ Other sessions of this user """

    if not user_id:
        return False

    already = db['online'].find_one({'id': user_id}, {'_id': True})
    return bool(already)

# Close session

def online_user_update(online):
    """ User data about online update """

    # TODO: Объединять сессии в онлайн по пользователю
    # TODO: Если сервер был остановлен, отслеживать сессию

    user = db['users'].find_one({'id': online['id']})
    if not user:
        return

    user['online'].append({'start': online['start'], 'stop': time.time()})
    db['users'].save(user)

def online_session_close(online):
    """ Close online session """

    # Remove from online users

    db['online'].remove(online['_id'])

async def online_emit_del(sio, user_id):
    """ Send sockets about deleting online users """

    user = db['users'].find_one({'id': user_id})
    if not user:
        return

    # Online users
    ## Other sessions of this user

    other = other_sessions(user_id)

    ## Emit to clients

    if not other:
        db_filter = {
            '_id': False,
            'id': True,
        }

        users_all = list(db['online'].find({}, db_filter))
        count = len({i['id'] for i in users_all})

        await sio.emit('online_del', {
            'count': count,
            'users': [{'id': user_id}], # ! Админам
        })


# Open session

async def online_emit_add(sio, user):
    """ Send sockets about adding online users """

    db_filter = {
        '_id': False,
        'id': True,
    }

    users_all = list(db['online'].find({}, db_filter))
    count = len({i['id'] for i in users_all})

    # Online users
    ## Emit this user to all users

    if user:
        # TODO: Full info for all / Full info only for admins

        user_data = {
            'id': user['id'],
            'login': user['login'],
            'name': user['name'],
            'surname': user['surname'],
        }

        if 'avatar' in user:
            user_data['avatar'] =  '/load/opt/' + user['avatar']
        else:
            user_data['avatar'] = 'user.png'

    else:
        user_data = []

    # Response

    res = {
        'count': count,
        'users': [user_data],
    }

    await sio.emit('online_add', res)

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
