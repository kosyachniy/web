"""
Functionality for working with Telegram
"""

from tgio import Telegram

from . import cfg


TG_TOKEN = cfg('tg.token')


tg = Telegram(TG_TOKEN)
