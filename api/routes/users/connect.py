from lib import log
from lib.sockets import sio


@sio.on("connect")
async def connect(sid, request, data):
    """Connect"""

    # TODO: ip = request['asgi.scope']['client'][0]

    log.debug("IN", sid)
