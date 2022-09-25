"""
The main functionality for the Telegram bot
"""

from libdev.cfg import cfg
from libdev.gen import generate
from libdev.aws import upload_file

from lib._api import auth, api
from lib.reports import report


__all__ = (
    'cfg',
    'generate',
    'auth', 'api',
    'upload_file',
    'report',
)
