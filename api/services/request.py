"""
Request info
"""

import time

from fastapi import Body
from pydantic import BaseModel
from libdev.codes import get_network, get_locale

from services.auth import get_user


class Request():
    """ Request container """
    def __init__(self, ip, socket, token, network, locale, sio=None):
        self.now = time.time()
        self.ip = ip # TODO: request.client.host,
        self.socket = socket
        self.network = get_network(network)
        self.locale = get_locale(locale)
        self.user, self.token = get_user(token, socket)
        self.sio = sio

class Type(BaseModel):
    ip: str = None
    socket: str = None
    token: str = None
    network: str = None
    locale: str = None
    sio: str = None

async def get_request(data: Type = Body(...)):
    """ Get request """
    return Request(**data.dict())
