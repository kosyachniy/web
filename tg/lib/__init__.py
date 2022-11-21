"""
The main functionality for the Telegram bot
"""

from libdev.cfg import cfg
from libdev.gen import generate
from libdev.aws import upload_file

# pylint: disable=import-error
from lib._variables import (
    locales, locales_chosen, tokens,
    user_ids, user_logins, user_statuses, user_names, user_titles,
)
from lib._api import auth, api
from lib.reports import report


__all__ = (
    'cfg',
    'generate',
    'locales', 'locales_chosen', 'tokens',
    'user_ids', 'user_logins', 'user_statuses', 'user_names', 'user_titles',
    'auth', 'api',
    'upload_file',
    'report',
)
