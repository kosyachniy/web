"""
Category model of DB object
"""

from libdev.lang import get_pure

from models import Base, Attribute
from lib.queue import get


def default_description(instance):
    """ Default description """
    return get_pure(instance.data).split('\n')[0]

class Category(Base):
    """ Category """

    _name = 'categories'
    _search_fields = {'title', 'data'}

    description = Attribute(types=str, default=default_description)
    parent = Attribute(types=int, default=0)
    url = Attribute(types=str)
    status = Attribute(types=int, default=1)
    token = Attribute(types=str)

    @classmethod
    def get_tree(cls, categories=None, parent=None, ids=None, **kwargs):
        """ Get tree of categories """

        if categories is None:
            categories = cls.get(**kwargs)

        if ids is None and parent is None:
            parent = 0

        tree = []

        for category in categories:
            if ids and ids != category.id:
                continue
            if category.parent is None:
                category.parent = 0
            if parent is not None and category.parent != parent:
                continue

            data = category.json()
            data['categories'] = cls.get_tree(categories, category.id)

            tree.append(data)

        return tree

    @classmethod
    def get_childs(cls, parent):
        """ Get childs of category """
        return get('category_childs').get(parent, []) + [parent]
