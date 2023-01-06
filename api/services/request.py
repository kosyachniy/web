"""
Request info
"""

import time

from fastapi import Body
from pydantic import BaseModel
from libdev.codes import get_network, get_locale


class Request():
    """ Request container """
    def __init__(self, ip, socket, network, locale):
        self.now = time.time()
        self.ip = ip # TODO: request.client.host,
        self.socket = socket
        self.network = get_network(network)
        self.locale = get_locale(locale)

class Type(BaseModel):
    ip: str = None
    socket: str = None
    network: str = None
    locale: str = None

async def get_request(data: Type = Body(...)):
    """ Get request """
    return Request(**data.dict())
