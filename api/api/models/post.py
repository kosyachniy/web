"""
Post model of DB object
"""

from . import Base, Attribute


class Post(Base):
    """ Post """

    db = 'posts'
    reactions = Attribute(dict, {
        'views': [],
        'likes': [],
        'reposts': [],
        'comments': [],
    }) # TODO: attributes
    cont = Attribute(str, '')
    cover = Attribute(str)
    # TODO: language
    # TODO: category
    # TODO: tags
    # TODO: author
    # TODO: source
    # TODO: language
