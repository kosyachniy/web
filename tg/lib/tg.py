"""
Functionality for working with Telegram
"""

from tgio import Telegram

from lib import cfg


TG_TOKEN = cfg('tg.token')


tg = Telegram(TG_TOKEN)
