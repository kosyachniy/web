"""
Reports functionality for the API
"""

from tgreports import Report

from api.lib import cfg


MODE = cfg('mode')
TG_TOKEN = cfg('tg.token')
BUG_CHAT = cfg('bug_chat')


report = Report(MODE, TG_TOKEN, BUG_CHAT)
