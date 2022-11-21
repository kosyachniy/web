"""
Base model of DB object
"""

from consys import make_base, Attribute
from consys.files import FileUploader

from lib import cfg


Base = make_base(
    host=cfg('mongo.host', 'db'),
    name=cfg('PROJECT_NAME'),
    login=cfg('mongo.user'),
    password=cfg('mongo.pass'),
)
# TODO: to S3
uploader = FileUploader('../data/load/', '/load/', cfg('side_optimized'))


__all__ = (
    'Base',
    'Attribute',
    'uploader',
)
