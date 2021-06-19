"""
Database ciphers
"""

# NOTE: ISO 639-1
LANGUAGES = (
    'en',
    'ru',
)

NETWORKS = (
    '',
    'web',
    'tg',
    'vk',
    'g',
    'fb',
)

USER_STATUSES = (
    'deleted',
    'blocked', # 'archive',
    'normal',
    'registered', # 'confirmed',
    'editor', # 'curator',
    'moderator',
    'admin',
    'owner',
)


def get_network(code):
    """ Get network code by cipher """

    if code in NETWORKS:
        return NETWORKS.index(code)

    if code in range(len(NETWORKS)):
        return code

    return 0

def get_language(code):
    """ Get language code by cipher """

    if code in LANGUAGES:
        return LANGUAGES.index(code)

    if code in range(len(LANGUAGES)):
        return code

    return 0
