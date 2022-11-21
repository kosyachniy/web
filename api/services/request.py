"""
Request info
"""

import time

from fastapi import Body
from pydantic import BaseModel
from libdev.codes import get_network as get_network_req

from routes.account.online import get_user


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
    jwt: str = None
    sio: str = None

async def get_request(data: Type = Body(...)):
    return Request(**data.dict())


class Type(BaseModel):
    network: str

def get_network(data: Type = Body(...)):
    return get_network_req(data.network)


class Type(BaseModel):
    ip: str

def get_ip(data: Type = Body(...)):
    return data.ip


class Type(BaseModel):
    token: str
    locale: str = None

def get_locale(data: Type = Body(...)):
    if data.locale is not None:
        return data.locale

    # user, _ = get_user(data.token)
    # return user.locale
