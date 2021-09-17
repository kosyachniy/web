"""
Functionality for working with Telegram
"""

import json

from tgio import Telegram


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    TG_TOKEN = sets['token']


tg = Telegram(TG_TOKEN)
dp = tg.dp
