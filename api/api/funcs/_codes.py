"""
Database ciphers
"""

import json


with open('sets.json', 'r', encoding='utf-8') as file:
    sets=json.loads(file.read())
    LOCALES = sets['locales']
    DEFAULT_LOCALE = sets['locale']


NETWORKS = (
    '',
    'web',
    'tg',
    'vk',
    'g',
    'fb',
)

USER_STATUSES = (
    'deleted', # not specified # Does not exist
    'blocked', # archive # Does not have access to resources
    'normal', # guest
    'registered', # confirmed # Save personal data & progress
    'editor', # curator # View reviews
    'verified', # Delete reviews
    'moderator', # Block users
    'admin', # Delete posts
    'owner', # Can't be blocked
)


def get_network(code):
    """ Get network code by cipher """

    if code in NETWORKS:
        return NETWORKS.index(code)

    if 0 <= code < len(NETWORKS):
        return code

    return 0

def get_language(code):
    """ Get language code by cipher """

    if code is None:
        return DEFAULT_LOCALE

    if code in LOCALES:
        return LOCALES.index(code)

    if code in range(len(LOCALES)):
        return code

    return 0
