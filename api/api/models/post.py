"""
Post model of DB object
"""

from api.models import Base, Attribute, uploader


class Post(Base):
    """ Post """

    # TODO: cont → data

    _name = 'posts'
    _search_fields = {'name', 'cont', 'tags'}

    cont = Attribute(types=str, default='', processing=uploader.reimg)
    reactions = Attribute(types=dict, default={
        'views': [], # TODO: + UTM
        'likes': [],
        'reposts': [],
        'comments': [],
    }) # TODO: attributes
    cover = Attribute(types=str, processing=uploader.image)
    tags = Attribute(types=list, default=[])
    # TODO: language
    # TODO: category
    # TODO: source
    # TODO: actions
