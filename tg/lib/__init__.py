"""
The main functionality for the Telegram bot
"""

from libdev.cfg import cfg
from libdev.gen import generate
from libdev.aws import upload_file

from lib._variables import (
    languages, languages_chosen, tokens,
    user_ids, user_logins, user_names, user_titles, user_statuses,
)
from lib._api import api
from lib.reports import report


__all__ = (
    'cfg',
    'generate',
    'languages', 'languages_chosen', 'tokens',
    'user_ids', 'user_logins', 'user_names', 'user_titles', 'user_statuses',
    'api',
    'upload_file',
    'report',
)
