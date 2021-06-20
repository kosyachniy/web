"""
The main functionality for the API
"""

import time
import string
import random

from ._types import check_params
from ._files import get_file, max_image, load_image, reimg
from ._codes import get_network, get_language
from ._online import online_back, online_start, online_user_update, \
                     online_session_close, online_emit_del
from ._users import get_user, get_status, get_status_condition, \
                    get_id, get_sids
from ._reports import report
from .mongodb import db


ALL_SYMBOLS = string.digits + string.ascii_letters

def generate(length: int = 32) -> str:
    """ Token / code generation """

    return ''.join(random.choice(ALL_SYMBOLS) for _ in range(length))

def next_id(name):
    """ Next DB ID """

    id_last = list(db[name].find({}, {'id': True, '_id': False}).sort('id', -1))

    if id_last:
        return id_last[0]['id'] + 1

    return 1

def get_date(text, template='%Y%m%d'):
    """ Get date from timestamp """

    return time.strftime(template, time.localtime(text))

def reduce_params(cont, params):
    """ Leave only the required fields for objects in the list """

    def only_params(element):
        return {i: element[i] for i in params}

    return list(map(only_params, cont))
