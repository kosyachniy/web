"""
Functionality for working with Telegram
"""

from tgio import Telegram

from api.lib import cfg


TG_TOKEN = cfg('tg.token')


tg = Telegram(TG_TOKEN)
