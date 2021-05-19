import os
import re
import time
import base64
import string
import random
import json

import requests
from PIL import Image, ExifTags

from api._func.mongodb import db
from api._func.tg_bot import send as send_tg
from api._error import ErrorSpecified, ErrorInvalid, ErrorType


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    SIDE_OPTIMIZED = sets['side_optimized']
    MODE = sets['mode']
    BUG_CHAT = sets['bug_chat']


# Check existence the file by name

def get_file(url, num):
    for i in os.listdir('../data/load/{}/'.format(url)):
        if re.search(r'^' + str(num) + '\.', i):
            return i

    return None

# Next image ID

def max_image(url):
    files = os.listdir(url)
    k = 0
    for i in files:
        j = re.findall(r'\d+', i)
        if len(j) and int(j[0]) > k:
            k = int(j[0])
    return k+1

# Upload image

def load_image(
    data, file_type=None, file_coding='base64', file_url='', file_id=None,
):
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

# Replace image in text

def reimg(text):
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

# Get user

def get_user(user_id):
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

        user_req['avatar'] = '/load/opt/' + user_req['avatar']
    else:
        user_req = 0

    return user_req

# Checking parameters

def check_params(data, filters): # ! Удалять другие поля (которых нет в списке)
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
                and not len(data[i[0]])

            if cond_null:
                raise ErrorInvalid(i[0])

        # Not all fields are filled
        elif i[1]:
            raise ErrorSpecified(i[0])

# Next DB ID

def next_id(name):
    try:
        db_filter = {'id': True, '_id': False}
        id_ = db[name].find({}, db_filter).sort('id', -1)[0]['id'] + 1
    except:
        id_ = 1

    return id_

# Convert language to code

def get_language(name):
    languages = ('en', 'ru', 'fi', 'es')

    if name in languages:
        name = languages.index(name)

    elif name not in range(len(languages)):
        name = 0

    return name

# Get available status for user

def get_status(user):
    if user['admin'] >= 6:
        return 0
    elif user['admin'] >= 5:
        return 1
    elif user['admin'] >= 3:
        return 3

    return 3 # !

def get_status_condition(user):
    if user['id']:
        return {
            '$or': [{
                'status': {'$gte': get_status(user)},
            }, {
                'user': user['id'],
            }]
        }

    else:
        return {
            'status': {'$gte': get_status(user)},
        }

# Define user by sid

def get_id(sid):
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

# All sid of this user

def get_sids(user):
    db_filter = {
        '_id': False,
        'sid': True,
    }

    user_sessions = db['online'].find({'id': user}, db_filter)

    return [i['sid'] for i in user_sessions]

# Get date from timestamp

def get_date(text, template='%Y%m%d'):
    return time.strftime(template, time.localtime(text))

# Leave only the required fields for objects in the list

def reduce_params(cont, params):
    def only_params(element):
        return {i: element[i] for i in params}

    return list(map(only_params, cont))

# Checking how long has been online

def online_back(user_id):
    online = db['online'].find_one({'id': user_id}, {'_id': True})
    if online:
        return 0

    db_filter = {'_id': False, 'online.stop': True}
    user = db['users'].find_one({'id': user_id}, db_filter)['online']

    last = max(i['stop'] for i in user)
    return time.time() - last

# Other sessions of this user

def other_sessions(user_id):
    if not user_id:
        return False

    already = db['online'].find_one({'id': user_id}, {'_id': True})
    return bool(already)

# Close session

def online_user_update(online):
    # User data update
    # ! Объединять сессии в онлайн по пользователю
    # ! Если сервер был остановлен, отслеживать сессию

    user = db['users'].find_one({'id': online['id']})
    if not user:
        return

    user['online'].append({'start': online['start'], 'stop': time.time()})
    db['users'].save(user)

def online_session_close(online):
    # Remove from online users

    db['online'].remove(online['_id'])

async def online_emit_del(sio, user_id):
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
        count = len(set([i['id'] for i in users_all]))

        await sio.emit('online_del', {
            'count': count,
            'users': [{'id': user_id}], # ! Админам
        })


# Open session

async def online_emit_add(sio, user):
    db_filter = {
        '_id': False,
        'id': True,
    }

    users_all = list(db['online'].find({}, db_filter))
    count = len(set([i['id'] for i in users_all]))

    # Online users
    ## Emit this user to all users

    await sio.emit('online_add', {
        'count': count,
        'users': [{
            'id': user['id'],
            'login': user['login'],
            'name': user['name'],
            'surname': user['surname'],
            'avatar': '/load/opt/' + user['avatar'],
        }] if user else [], # ! Full info for all / Full info only for admins
    })

# Report

SYMBOLS = ['🟢', '🟡', '🔴', '❗️', '✅']
TYPES = ['INFO', 'WARNING', 'ERROR', 'CRITICAL', 'IMPORTANT']

def report(text, type_=0, additional=''):
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
