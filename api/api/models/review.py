"""
Review model of DB object
"""

from . import Base, Attribute, uploader


class Review(Base):
    """ Review """

    _name = 'reviews'
    _search_fields = {'name', 'cont'}

    cont = Attribute(types=str, default='', processing=uploader.reimg)
    network = Attribute(types=int, default=0)
    # TODO: link
    # TODO: executor
    # TODO: category / type : system / custom / ...
