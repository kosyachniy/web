"""
Token model of DB object
"""

from . import Base, Attribute


class Token(Base):
    """ Token """

    _name = 'tokens'

    id = Attribute(types=str)
