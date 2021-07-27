"""
Socket model of DB object
"""

from . import Base, Attribute


class Socket(Base):
    """ Socket """

    _db = 'sockets'

    id = Attribute(types=str)
    token = Attribute(types=str)
