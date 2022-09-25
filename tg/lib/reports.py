"""
Reports functionality for the Telegram bot
"""

from libdev.cfg import cfg
from tgreports import Report


report = Report(cfg('mode'), cfg('tg.token'), cfg('bug_chat'))
