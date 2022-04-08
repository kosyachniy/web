"""
Functionality for working with Telegram
"""

from tgio import Telegram

from api.lib import cfg


tg = Telegram(cfg('tg.token'))
