"""
Base model of DB object
"""

from consys import make_base, Attribute

from api.lib import cfg


HOST = cfg('mongo.host')
NAME = cfg('PROJECT_NAME')
LOGIN = cfg('mongo.login')
PASSWORD = cfg('mongo.password')


Base = make_base(HOST, NAME, LOGIN, PASSWORD)


__all__ = (
    'Base',
    'Attribute',
)
