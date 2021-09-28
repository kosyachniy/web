"""
Base model of DB object
"""

import json

from consys import make_base, Attribute


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['mongo']
    host = sets['host']
    name = sets['db']
    login = sets['login']
    password = sets['password']


Base = make_base(host, name, login, password)


__all__ = (
    'Base',
    'Attribute',
)
