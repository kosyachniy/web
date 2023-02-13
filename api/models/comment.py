"""
Comment model of DB object
"""

from models import Base, Attribute


class Comment(Base):
    """ Comment """

    _name = 'comments'
    _search_fields = {'data'}

    data = Attribute(types=str, default='')
    parent = Attribute(types=int, default=0)
    reactions = Attribute(types=dict)
    post = Attribute(types=int)
    status = Attribute(types=int, default=1)
    token = Attribute(types=str)
