"""
Token model of DB object
"""

from . import Base, Attribute


class Token(Base):
    """ Token """

    _db = 'tokens'

    id = Attribute(types=str)
