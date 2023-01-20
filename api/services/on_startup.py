"""
Tasks on start
"""

from services.cache import cache_categories


def on_startup():
    """ Tasks on start """

    cache_categories()
