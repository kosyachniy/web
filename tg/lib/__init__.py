"""
The main functionality for the Telegram bot
"""

from libdev.cfg import cfg
from libdev.gen import generate

from lib._variables import languages, languages_chosen, tokens, ids
from lib._api import api
from lib.reports import report


__all__ = (
    'cfg',
    'generate',
    'languages', 'languages_chosen', 'tokens', 'ids',
    'api',
    'report'
)
