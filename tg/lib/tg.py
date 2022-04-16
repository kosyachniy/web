"""
Functionality for working with Telegram
"""

from tgio import Telegram

from lib import cfg


tg = Telegram(cfg('tg.token'))
