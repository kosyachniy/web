"""
Reports functionality for the Telegram bot
"""

from tgreports import Report

from lib import cfg


MODE = cfg('mode')
TG_TOKEN = cfg('tg.token')
BUG_CHAT = cfg('bug_chat')


report = Report(MODE, TG_TOKEN, BUG_CHAT)
