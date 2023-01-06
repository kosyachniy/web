"""
Socket model of DB object
"""

from models import Base, Attribute


class Socket(Base):
    """ Socket """

    _name = 'sockets'

    id = Attribute(types=str)
    token = Attribute(types=str)
