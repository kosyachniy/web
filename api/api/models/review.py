"""
Review model of DB object
"""

from . import Base, Attribute


class Review(Base):
    """ Review """

    _db = 'reviews'
    cont = Attribute(str, '')
    author = Attribute(int)
    network = Attribute(int, 0)
    # TODO: link
    # TODO: executor
