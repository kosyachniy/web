"""
Post model of DB object
"""

from . import Base, Attribute
from ..funcs import load_image, reimg


class Post(Base):
    """ Post """

    _name = 'posts'
    _search_fields = {'name', 'cont', 'tags'}

    cont = Attribute(types=str, default='', processing=reimg)
    reactions = Attribute(types=dict, default={
        'views': [], # TODO: + UTM
        'likes': [],
        'reposts': [],
        'comments': [],
    }) # TODO: attributes
    cover = Attribute(types=str, processing=load_image)
    tags = Attribute(types=list, default=[])
    # TODO: language
    # TODO: category
    # TODO: source
    # TODO: actions
