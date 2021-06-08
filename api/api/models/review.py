"""
Review model of DB object
"""

from . import Base, Attribute


class Review(Base):
    """ Review """

    _db = 'reviews'
    cont = Attribute(str, '')
    network = Attribute(int, 0)
    # TODO: link
    # TODO: executor
