"""
Sending SMS messages
"""

import json


with open('sets.json', 'r', encoding='utf-8') as file:
    sets = json.loads(file.read())['smsc']
    LOGIN = sets['login']
    PASSWORD = sets['password']

# TODO: Use pip/smsc