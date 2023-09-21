"""
Post model of DB object
"""

import time

from libdev.time import get_time
from libdev.lang import get_pure, to_url

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

def default_description(instance):
    """ Default description """
    return get_pure(instance.data).split('\n')[0]

def default_url(instance):
    """ Default url """
    url = to_url(instance.title) or ""
    if url:
        url += "-"
    return url + f"{instance.id}"

class Post(Base):
    """ Post """

    _name = 'posts'
    _search_fields = {'title', 'data', 'tags'}

    title = Attribute(types=str, default=default_title)
    description = Attribute(types=str, default=default_description)
    data = Attribute(types=str, default='')
    category = Attribute(types=int, default=0)
    tags = Attribute(types=list)
    source = Attribute(types=str)
    url = Attribute(types=str, default=default_url)
    status = Attribute(types=int, default=1)
    token = Attribute(types=str)
