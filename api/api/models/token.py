"""
Token model of DB object
"""

from . import Base, Attribute


class Token(Base):
    """ Token """

    db = 'tokens'
    id = Attribute(str)
    user = Attribute(int)
