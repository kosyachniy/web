"""
Post model of DB object
"""

from api.models import Base, Attribute


class Post(Base):
    """ Post """

    _name = 'posts'
    _search_fields = {'title', 'data', 'tags'}

    reactions = Attribute(types=dict, default={
        'views': [], # TODO: + UTM
        'likes': [],
        'reposts': [],
        'comments': [],
    }) # TODO: attributes
    cover = Attribute(types=str)
    tags = Attribute(types=list)
    # TODO: language
    # TODO: category
    # TODO: source
    # TODO: actions
