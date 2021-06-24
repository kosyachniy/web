"""
Post model of DB object
"""

from . import Base, Attribute


class Post(Base):
    """ Post """

    _db = 'posts'
    cont = Attribute(types=str, default='')
    reactions = Attribute(types=dict, default={
        'views': [], # TODO: + UTM
        'likes': [],
        'reposts': [],
        'comments': [],
    }) # TODO: attributes
    cover = Attribute(types=str)
    tags = Attribute(types=list, default=[])
    # TODO: language
    # TODO: category
    # TODO: source
    # TODO: actions
