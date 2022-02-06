"""
The API
"""

import time

from api.lib import get_network, get_language, report
from api.methods import call
from api.methods.account.online import get_user


class Request():
    """ Request container """

    def __init__(self, ip, socket, token, network, locale, jwt=None, sio=None):
        self.timestamp = time.time()
        self.ip = ip
        self.socket = socket
        self.token = token
        self.network = get_network(network)
        self.locale = get_language(locale)
        self.user = get_user(token, socket, jwt)
        self.sio = sio


class API():
    """ API """

    def __init__(self, sio=None):
        self.sio = sio

    # pylint: disable=too-many-arguments
    async def method(
        self,
        name,
        data=None,
        ip=None,
        socket=None,
        token=None,
        network=0,
        locale=0,
        jwt=None,
    ):
        """ Call API method """

        if (
            socket is None and token is None
            and jwt is None and name != 'account.app'
        ):
            await report.warning("There is no socket id and token", {
                'method': name,
                'ip': ip,
            })

        if not data:
            data = {}

        # print(name, data, ip, socket, token, network, locale)

        request = Request(ip, socket, token, network, locale, jwt, self.sio)

        # # Action tracking
        # Track(
        #     title=name,
        #     data=data,
        #     context=request,
        #     user=request.user,
        # }.save()

        # API method
        return await call(name, request, data)
