"""
Reports functionality for the Telegram bot
"""

import json

from tgreports import Report


with open('sets.json', 'r', encoding='utf-8') as file:
    sets = json.loads(file.read())
    MODE = sets['mode']
    TG_TOKEN = sets['tg']['token']
    BUG_CHAT = sets['bug_chat']


report = Report(MODE, TG_TOKEN, BUG_CHAT)
