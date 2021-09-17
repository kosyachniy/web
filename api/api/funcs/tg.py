"""
Functionality for working with Telegram
"""

from tgio import Telegram
import json


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    TG_TOKEN = sets['token']


tg = Telegram(TG_TOKEN)
dp = tg.dp
