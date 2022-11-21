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
    def __init__(self, ip, socket, token, network, locale, jwt=None, sio=None):
        self.now = time.time()
        self.ip = ip
        self.socket = socket
        self.network = get_network(network)
        self.locale = get_locale(locale)
        self.user, self.token = get_user(token, socket, jwt)
        self.sio = sio

class Type(BaseModel):
    ip: str
    socket: str
    token: str
    network: str
    locale: str
    jwt: dict = None
    sio: str = None

async def get_request(data: Type = Body(...)):
    """ Get request """
    return Request(**data.dict())
