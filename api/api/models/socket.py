"""
Socket model of DB object
"""

from . import Base, Attribute


class Socket(Base):
    """ Socket """

    _db = 'sockets'
    id = Attribute(str)
    token = Attribute(str)
