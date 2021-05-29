"""
Review model of DB object
"""

from . import Base, Attribute


class Review(Base):
    """ Review """

    db = 'reviews'
    cont = Attribute(str, '')
    author = Attribute(int)
    # TODO: link
    # TODO: executor
