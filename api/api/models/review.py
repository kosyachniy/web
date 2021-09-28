"""
Review model of DB object
"""

from . import Base, Attribute
from ..funcs import reimg


class Review(Base):
    """ Review """

    _name = 'reviews'
    _search_fields = {'name', 'cont'}

    cont = Attribute(types=str, default='', processing=reimg)
    network = Attribute(types=int, default=0)
    # TODO: link
    # TODO: executor
    # TODO: category / type : system / custom / ...
