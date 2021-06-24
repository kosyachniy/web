"""
Review model of DB object
"""

from . import Base, Attribute


class Review(Base):
    """ Review """

    _db = 'reviews'
    cont = Attribute(types=str, default='')
    network = Attribute(types=int, default=0)
    # TODO: link
    # TODO: executor
