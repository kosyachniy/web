"""
Base model of DB object
"""

from consys import make_base, Attribute
from consys.files import FileUploader

from ..lib import cfg


HOST = cfg('mongo.host')
NAME = cfg('mongo.db')
LOGIN = cfg('mongo.login')
PASSWORD = cfg('mongo.password')
SIDE_OPTIMIZED = cfg('side_optimized')


Base = make_base(HOST, NAME, LOGIN, PASSWORD)
uploader = FileUploader('../data/load/', '/load/', SIDE_OPTIMIZED)


__all__ = (
    'Base',
    'Attribute',
    'uploader',
)
