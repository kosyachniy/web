"""
Post model of DB object
"""

import time

from libdev.time import get_time

from models import Base, Attribute
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

    image = Attribute(types=str)
    title = Attribute(types=str, default=default_title)
    data = Attribute(types=str, default='')
    category = Attribute(types=int, default=0)
    reactions = Attribute(types=dict, default={
        'views': [], # TODO: + UTM
        'likes': [],
        'reposts': [],
        'comments': [],
    }) # TODO: attributes
    tags = Attribute(types=list)
    source = Attribute(types=str)
    status = Attribute(types=int, default=1)
    token = Attribute(types=str)
