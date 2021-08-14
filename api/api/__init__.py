"""
The API
"""

# Libraries
## System
import time

## Local
from .funcs import get_network, get_language, get_user
from .methods import call
from .background import background


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
        background(self.sio)

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
