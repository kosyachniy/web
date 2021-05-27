"""
The API
"""

# Libraries
## System
import time

## Local
from .funcs import get_language
from .funcs.mongodb import db
from .background import background
from .errors import ErrorWrong

import api.methods.account as account
import api.methods.users as users
import api.methods.feedback as feedback
import api.methods.posts as posts

# import importlib
# import pkgutil

# def import_submodules(module):
#     """ Import all submodules of a module """

#     for loader, module_name, is_pkg in pkgutil.walk_packages(
#         module.__path__, module.__name__ + '.'
#     ):
#         importlib.import_module(module_name)

# importlib.import_module('.methods', 'methods')
# import_submodules(api.methods)


class API():
    """ API """

    def __init__(self, client, sio=None):
        self.client = client
        self.sio = sio

        # Background processes
        background(self.sio)

    # pylint: disable=C0103
    async def method(
        self, name, params={}, ip=None, sid=None, token=None, language=0,
    ):
        """ Called API method """

        # TODO: network

        self.timestamp = time.time()
        self.ip = ip
        self.sid = sid
        self.token = token
        self.language = get_language(language)

        # User recognition

        self.user = {
            'id': 0,
            'admin': 2,
        }

        if token:
            db_filter = {'id': True, '_id': False}
            user_id = db['tokens'].find_one({'token': token}, db_filter)

            if user_id and user_id['id']:
                user = db['users'].find_one({'id': user_id['id']})

                if user:
                    self.user = user

        # Remove extra indentation

        for i in params:
            if type(params[i]) == str:
                params[i] = params[i].strip()

        # # Action tracking

        # req = {
        #     'time': self.timestamp,
        #     'user': self.user['id'],
        #     'ip': self.ip,
        #     'method': name,
        #     'params': params,
        # }

        # db['actions'].insert_one(req)

        # API method

        try:
            module, method_name = name.split('.')
            func = getattr(globals()[module], method_name)
        except:
            raise ErrorWrong('method')

        # Request

        return await func(self, **params)
