"""
Post model of DB object
"""

import time

from libdev.time import get_time

from models import Base, Attribute, uploader
from lib import cfg


def default_title(instance):
    """ Default title """
    text_time = get_time(
        instance.created or time.time(),
        '%d.%m.%Y',
        cfg('timezone'),
    )
    return f"Черновик от {text_time}"


class Post(Base):
    """ Post """

    _name = 'posts'
    _search_fields = {'title', 'data', 'tags'}

    image = Attribute(types=str, processing=uploader.image)
    title = Attribute(types=str, default=default_title)
    data = Attribute(types=str, default='', processing=uploader.reimg)
    reactions = Attribute(types=dict, default={
        'views': [], # TODO: + UTM
        'likes': [],
        'reposts': [],
        'comments': [],
    }) # TODO: attributes
    tags = Attribute(types=list)
    status = Attribute(types=int, default=1)
    # TODO: locale
    # TODO: category
    # TODO: source
    # TODO: actions
