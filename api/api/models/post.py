"""
Post model of DB object
"""

import time

from libdev.time import get_time

from api.lib import cfg
from api.models import Base, Attribute, uploader


def default_title(instance):
    """ Default resume title """
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
    # TODO: language
    # TODO: category
    # TODO: source
    # TODO: actions
