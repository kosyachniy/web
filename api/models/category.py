"""
Category model of DB object
"""

from models import Base, Attribute


class Category(Base):
    """ Category """

    _name = 'categories'
    _search_fields = {'title', 'data'}

    image = Attribute(types=str)
    title = Attribute(types=str)
    data = Attribute(types=str, default='')
    locale = Attribute(types=str)
    status = Attribute(types=int, default=1)
    token = Attribute(types=str)
