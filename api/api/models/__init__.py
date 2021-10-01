"""
Base model of DB object
"""

import json

from consys import make_base, Attribute
from consys.files import FileUploader


with open('sets.json', 'r', encoding='utf-8') as file:
    sets = json.loads(file.read())
    host = sets['mongo']['host']
    name = sets['mongo']['db']
    login = sets['mongo']['login']
    password = sets['mongo']['password']
    side_optimized = sets['side_optimized']


Base = make_base(host, name, login, password)
uploader = FileUploader('../data/load/', '/load/', side_optimized)


__all__ = (
    'Base',
    'Attribute',
    'uploader',
)
