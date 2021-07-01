"""
The main functionality for the API
"""

import time

from ._types import check_params
from ._files import get_file, max_image, load_image, reimg
from ._codes import get_network, get_language
from ._generate import generate, generate_password
from ._online import get_user, online_back, online_start, online_stop
from ._reports import report
from .mongodb import db


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
