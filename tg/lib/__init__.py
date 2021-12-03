"""
The main functionality for the Telegram bot
"""

from libdev.cfg import cfg
from libdev.gen import generate

from lib._variables import (
    languages, languages_chosen, tokens,
    user_ids, user_logins, user_names, user_titles,
)
from lib._api import api
from lib.reports import report


__all__ = (
    'cfg',
    'generate',
    'languages', 'languages_chosen', 'tokens',
    'user_ids', 'user_logins', 'user_names', 'user_titles',
    'api',
    'report'
)
