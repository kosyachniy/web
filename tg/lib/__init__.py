"""
The main functionality for the Telegram bot
"""

from libdev.cfg import cfg
from libdev.gen import generate

from ._variables import languages, languages_chosen, tokens, ids
from ._api import api
from .reports import report


__all__ = (
    'cfg',
    'generate',
    'languages', 'languages_chosen', 'tokens', 'ids',
    'api',
    'report'
)
