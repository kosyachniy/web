"""
Token model of DB object
"""

from api.models import Base, Attribute


class Token(Base):
    """ Token """

    _name = 'tokens'

    id = Attribute(types=str)
