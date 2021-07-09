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
    'deleted', # not specified # Does not exist
    'blocked', # archive # Does not have access to resources
    'normal',
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
