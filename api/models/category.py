"""
Category model of DB object
"""

from models import Base, Attribute


class Category(Base):
    """ Category """

    _name = 'categories'
    _search_fields = {'title', 'data'}

    parent = Attribute(types=int, default=0)
    status = Attribute(types=int, default=1)
    token = Attribute(types=str)

    @classmethod
    def get_tree(cls, categories=None, parent=0, **kwargs):
        """ Get tree of categories """

        if categories is None:
            categories = cls.get(**kwargs)

        if parent is None:
            parent = 0

        tree = []

        for category in categories:
            if category.parent is None:
                category.parent = 0
            if category.parent != parent:
                continue

            data = category.json()
            data['categories'] = cls.get_tree(categories, category.id)

            tree.append(data)

        return tree
