"""
User model of DB object
"""

import re
import hashlib

from . import Base, Attribute
from ..funcs import load_image, get_language
from ..funcs.mongodb import db


RESERVED = {
    'admin', 'admins', 'administrator', 'administrators', 'administration',
    'author', 'support', 'manager', 'client',
    'account', 'profile', 'login', 'sign', 'signin', 'signup', 'password',
    'root', 'server', 'info', 'no-reply',
    'dev', 'test', 'tests', 'tester', 'testers',
    'user', 'users', 'bot', 'bots', 'robot', 'robots',
    'phone', 'code', 'codes', 'mail',
    'google', 'facebook', 'telegram', 'instagram', 'twitter',
    'anon', 'anonym', 'anonymous', 'undefined', 'ufo',
}


def default_login(instance):
    """ Default login value """

    return f"id{instance.id}"

def check_login(id_, cont):
    """ Login checking """

    # Already registered
    users = db.users.find_one({'login': cont}, {'_id': True, 'id': True})
    if users and users['id'] != id_:
        return False

    # Invalid login

    cond_length = not 3 <= len(cont) <= 20
    cond_symbols = re.findall(r'[^a-zA-Z0-9_]', cont)
    cond_letters = not re.findall(r'[a-zA-Z]', cont)

    if cond_length or cond_symbols or cond_letters:
        return False

    # System reserved

    cond_id = cont[:2] == 'id' and cont[2:].isalpha() and int(cont[2:]) != id_
    cond_reserved = cont in RESERVED

    if cond_id or cond_reserved:
        return False

    return True

# pylint: disable=unused-argument
def check_password(id_, cont):
    """ Password checking """

    # Invalid password

    cond_length = not 6 <= len(cont) <= 40
    cond_symbols = re.findall(r'[^a-zA-Z0-9!@#$%&*-+=,./?|]~', cont)
    cond_letters = not re.findall(r'[a-zA-Z]', cont)
    cond_digits = not re.findall(r'[0-9]', cont)

    if cond_length or cond_symbols or cond_letters or cond_digits:
        return False

    return True

def process_password(cont):
    """ Password processing """

    return hashlib.md5(bytes(cont, 'utf-8')).hexdigest()

# pylint: disable=unused-argument
def check_name(id_, cont):
    """ Name checking """

    return cont.isalpha()

# pylint: disable=unused-argument
def check_surname(id_, cont):
    """ Surname checking """

    return cont.replace('-', '').isalpha()

# pylint: disable=unused-argument
def check_phone(id_, cont):
    """ Phone checking """

    return 11 <= len(str(cont)) <= 18

def pre_process_phone(cont):
    """ Phone number pre-processing """

    cont = str(cont)

    if not cont:
        return 0

    if cont[0] == '8':
        cont = '7' + cont[1:]

    cont = re.sub(r'[^0-9]', '', cont)

    if not cont:
        return 0

    return int(cont)

def check_mail(id_, cont):
    """ Mail checking """

    # Invalid
    if re.match(r'.+@.+\..+', cont) is None:
        return False

    # Already registered
    users = db.users.find_one({'mail': cont}, {'_id': False, 'id': True})
    if users and users['id'] != id_:
        return False

    return True

def process_title(cont):
    """ Make a value with a capital letter """

    return cont.title()

def process_lower(cont):
    """ Make the value in lowercase """

    return cont.lower()

def default_status(instance):
    """ Default status """

    if instance.id:
        return 3

    return 2

# def default_referal_code():
#     ALL_SYMBOLS = string.ascii_lowercase + string.digits
#     generate = lambda length=8: ''.join(
#         random.choice(ALL_SYMBOLS) for _ in range(length)
#     )
#     return generate()


class User(Base):
    """ User """

    _db = 'users'
    _search_fields = {
        'login',
        'name',
        'surname',
        'phone',
        'mail',
        'description',
        # 'actions',
    }

    login = Attribute(
        types=str,
        default=default_login,
        checking=check_login,
        pre_processing=process_lower,
        ignore=True,
    )
    password = Attribute(
        types=str,
        checking=check_password,
        processing=process_password,
    )
    avatar = Attribute(types=str, processing=load_image)
    name = Attribute(
        types=str,
        checking=check_name,
        processing=process_title,
        ignore=True,
    )
    surname = Attribute(
        types=str,
        checking=check_surname,
        processing=process_title,
        ignore=True,
    )
    phone = Attribute(
        types=int,
        checking=check_phone,
        pre_processing=pre_process_phone,
    )
    phone_verified = Attribute(types=bool, default=True)
    mail = Attribute(
        types=str,
        checking=check_mail,
        pre_processing=process_lower,
    )
    mail_verified = Attribute(types=bool, default=True)
    social = Attribute(types=list, default=[]) # TODO: list[{}] # TODO: checking
    description = Attribute(types=str)
    language = Attribute(
        types=int,
        default=0,
        pre_processing=get_language,
    )
    status = Attribute(types=int, default=default_status)
    actions = Attribute(types=list, default=[]) # TODO: list[dict]
    online = Attribute(types=list, default=[]) # TODO: list[tuple]
    # TODO: UTM / promo
    # TODO: discount
    # TODO: balance
    # TODO: subscription
    # TODO: rating
    # TODO: referal_parent
    # TODO: referal_code
    # TODO: channels
    # TODO: attempts (password)
    # TODO: middle name

    # TODO: del Base.user
