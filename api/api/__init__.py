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


# pylint: disable=R0902,R0903,W0201
class API():
    """ API """

    def __init__(self, client, sio=None):
        self.client = client
        self.sio = sio

        # Background processes
        background(self.sio)

    # pylint: disable=C0103,R0913
    async def method(
        self,
        name,
        params=None,
        ip=None,
        socket=None,
        token=None,
        network=0,
        language=0,
    ):
        """ Call API method """

        if not params:
            params = {}

        # print(name, params)

        self.timestamp = time.time()
        self.ip = ip
        self.socket = socket
        self.token = token
        self.network = get_network(network)
        self.language = get_language(language)
        self.user = get_user(token)

        # # Action tracking

        # action = Action(
        #     user=self.user.id,
        #     token=self.token,
        #     socket=self.socket,
        #     ip=self.ip,
        #     method=name,
        #     params=params,
        # }

        # action.save()

        # API method

        return await call(name, self, params)
