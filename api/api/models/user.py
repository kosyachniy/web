"""
User model of DB object
"""

import re
import hashlib

from . import Base, Attribute
from ..funcs import load_image
from ..funcs.mongodb import db


RESERVED = (
    'admin', 'admins', 'administrator', 'administrators', 'administration',
    'author', 'support', 'manager', 'client',
    'account', 'profile', 'login', 'password',
    'root', 'server', 'info',  'no-reply',
    'dev', 'test', 'tests', 'tester', 'testers',
    'user', 'users', 'bot', 'bots', 'robot', 'robots',
    'phone', 'code', 'codes', 'mail',
    'google', 'facebook', 'telegram', 'instagram', 'twitter',
    'anon', 'anonym', 'anonymous', 'undefined', 'ufo',
)


def default_login(instance):
    """ Default login value """

    return f"id{instance.id}"

def check_login(id_, cont):
    """ Login checking """

    # Already registered

    users = db['users'].find_one({'login': cont}, {'_id': True, 'id': True})
    if users and users['id'] != id_:
        return False

    # Invalid login

    cond_length = not 3 <= len(cont) <= 20
    cond_symbols = re.findall(r'[^a-z0-9_]', cont)
    cond_letters = not re.findall(r'[a-z]', cont)

    if cond_length or cond_symbols or cond_letters:
        return False

    # System reserved

    cond_id = cont[:2] == 'id'
    cond_reserved = cont in RESERVED

    if cond_id or cond_reserved:
        return False

    return True

def check_password(id_, cont):
    """ Password checking """

    # Invalid password

    cond_length = not 6 <= len(cont) <= 40
    cond_symbols = re.findall(r'[^a-zA-Z0-9!@#$%&*-+=,./?|~]', cont)
    cond_letters = not re.findall(r'[a-zA-Z]', cont)
    cond_digits = not re.findall(r'[0-9]', cont)

    if cond_length or cond_symbols or cond_letters or cond_digits:
        return False

    return True

def process_password(cont):
    """ Password processing """

    return hashlib.md5(bytes(cont, 'utf-8')).hexdigest()

def check_name(id_, cont):
    """ Name checking """

    return cont.isalpha()

def process_name(cont):
    """ Name processing """

    return cont.title()

def check_surname(id_, cont):
    """ Surname checking """

    return cont.replace('-', '').isalpha()

def process_surname(cont):
    """ Surname processing """

    return cont.title()

def check_phone(id_, cont):
    """ Phone checking """

    return 11 <= len(str(cont)) <= 18

def pre_process_phone(cont):
    """ Phone number pre-processing """

    cont = str(cont)

    if not len(cont):
        return ''

    if cont[0] == '8':
        cont = '7' + cont[1:]

    return int(re.sub(r'[^0-9]', '', cont))

def check_mail(id_, cont):
    """ Mail checking """

    # Invalid
    if re.match(r'.+@.+\..+', cont) is None:
        return False

    # Already registered
    users = db['users'].find_one({'mail': cont}, {'_id': False, 'id': True})
    if users and users['id'] != id_:
        return False

    return True

# def default_referal_code():
#     ALL_SYMBOLS = string.ascii_lowercase + string.digits
#     generate = lambda length=8: ''.join(
#         random.choice(ALL_SYMBOLS) for _ in range(length)
#     )
#     return generate()


class User(Base):
    """ User """

    db = 'users'
    login = Attribute(str, default_login, checking=check_login)
    password = Attribute(
        str,
        checking=check_password,
        processing=process_password,
    )
    avatar = Attribute(str, processing=load_image)
    name = Attribute(
        str,
        checking=check_name,
        processing=process_name,
    )
    surname = Attribute(
        str,
        checking=check_surname,
        processing=process_surname,
    )
    phone = Attribute(
        int,
        checking=check_phone,
        pre_processing=pre_process_phone,
    )
    mail = Attribute(str, checking=check_mail)
    social = Attribute(list, []) # TODO: list[dict] # TODO: checking
    description = Attribute(str)
    language = Attribute(int, 0)
    status = Attribute(int, 2) # TODO: or 3
    funnel = Attribute(list, []) # TODO: list[dict]
    online = Attribute(list, []) # TODO: list[tuple]
    # TODO: balance
    # TODO: rating
    # TODO: referal_parent
    # TODO: referal_code
