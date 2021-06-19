"""
Reports functionality for the API
"""

import json

from .tg_bot import send as send_tg


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    MODE = sets['mode']
    BUG_CHAT = sets['bug_chat']

SYMBOLS = ['🟢', '🟡', '🔴', '❗️', '✅']
TYPES = ['INFO', 'WARNING', 'ERROR', 'CRITICAL', 'IMPORTANT']


def report(text, type_=0, additional=''):
    """ Report logs and notifications on Telegram chat or in log files """

    if MODE != "PROD" and type_ == 0:
        return

    preview = f"{SYMBOLS[type_]} {MODE} {TYPES[type_]}\n---------------\n"
    text = preview + text
    if additional:
        text_with_additional = text + '\n\n' + str(additional)
    else:
        text_with_additional = text

    try:
        send_tg(BUG_CHAT, text_with_additional, markup=None)
    except Exception as error:
        if additional:
            print("❗️❗️❗️", error)
            print(additional)

            try:
                send_tg(BUG_CHAT, text, markup=None)
            except Exception as error:
                print("❗️❗️❗️", error)
                print(type_, text)

        else:
            print("❗️❗️❗️", error)
            print(type_, text)
