"""
Base model of DB object
"""

from consys import make_base, Attribute

from api.lib import cfg


HOST = cfg('mongo.host')
NAME = cfg('PROJECT_NAME')
LOGIN = cfg('mongo.user')
PASSWORD = cfg('mongo.pass')


Base = make_base(HOST, NAME, LOGIN, PASSWORD)


__all__ = (
    'Base',
    'Attribute',
)
