"""
The API
"""

import asyncio
import time
import json

from libdev.codes import get_network, get_language

from .lib.reports import report
from .methods import call
from .methods.account.online import get_user
from .background import background


with open('sets.json', 'r', encoding='utf-8') as file:
    env_sets=json.loads(file.read())
    DEFAULT_LOCALE = env_sets['locale']


class Request():
    """ Request container """

    def __init__(self, ip, socket, token, network, locale):
        self.timestamp = time.time()
        self.ip = ip
        self.socket = socket
        self.token = token
        self.network = get_network(network)
        self.locale = get_language(locale)
        self.user = get_user(token)

        if self.locale is None:
            self.locale = DEFAULT_LOCALE


class API():
    """ API """

    def __init__(self, sio=None, **sets):
        # TODO: Libraries

        self.sio = sio

        # Settings
        self.client = sets['client']

        # Networks
        self.tg = sets['tg']
        self.vk = sets['vk']
        self.google = sets['google']

        # Background processes
        asyncio.create_task(background(sio))

    async def method(
        self,
        name,
        data=None,
        ip=None,
        socket=None,
        token=None,
        network=0,
        locale=0,
    ):
        """ Call API method """

        if socket is None and token is None:
            report.warning("There is no socket id and token", {'method': name})

        if not data:
            data = {}

        # print(name, data, ip, socket, token, network, locale)

        request = Request(ip, socket, token, network, locale)

        # # Action tracking

        # action = Action(
        #     name=name,
        #     data=data,
        #     request=request,
        # }

        # action.save()

        # API method
        return await call(name, self, request, data)
