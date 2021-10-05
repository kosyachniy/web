"""
API functionality for the Telegram bot
"""

# Libraries
## System
import json
import time

## External
import requests
from libdev.gen import generate

## Local
from ._variables import languages, languages_chosen, tokens, ids
from ._reports import report


# Params
with open('sets.json', 'r', encoding='utf-8') as file:
    sets = json.loads(file.read())
    SERVER_LINK = sets['server']

LOG_LIMIT = 330


# Funcs
async def api(chat, method, data=None):
    """ API request """

    chat_id = chat.id

    if data is None:
        data = {}

    if chat_id not in tokens:
        res = await auth(chat)

        if res is None:
            return 1, None

    req = {
        'method': method,
        'params': data,
        'token': tokens[chat_id],
        'network': 'tg',
        'locale': languages[chat_id],
    }

    await report.debug(
        "API request",
        {
            'user': chat_id,
            'data': json.dumps(req, ensure_ascii=False)[:LOG_LIMIT],
        }
    )

    # UGLY: Rewrite `while True` & `time.sleep`
    while True:
        res = requests.post(SERVER_LINK, json=req)

        if res.status_code != 502:
            break

        time.sleep(5)

    if res.status_code != 200:
        await report.error(
            "API response",
            {
                'user': chat_id,
                'method': method,
                'params': data,
                'token': tokens[chat_id],
                'locale': languages[chat_id],
                'error': res.status_code,
            }
        )
        return 1, None

    res = res.json()

    await report.debug(
        "API response",
        {
            'user': chat_id,
            'data': res,
        }
    )

    return res['error'], res['data']

async def auth(chat) -> bool:
    """ User authentication """

    chat_id = chat.id

    if chat_id in ids:
        return False

    # Default settings
    if chat_id not in languages:
        languages[chat_id] = 1 # TODO: 0

    ## Token
    token = generate()
    tokens[chat_id] = token

    ## Call the API
    error, data = await api(chat, 'account.bot', {
        'user': chat.id,
        'name': chat.first_name or chat.title or None,
        'surname': chat.last_name or None,
        'login': chat.username or None,
    })

    # Errors
    if error:
        await report.error(
            "Authorization",
            {
                'user': chat.id,
                'name': chat.first_name or chat.title or None,
                'surname': chat.last_name or None,
                'login': chat.username or None,
                'error': error,
                'data': data,
            }
        )

        del tokens[chat_id]
        return

    ## Update global variables

    ids[chat_id] = data['id']

    if 'language' in data['social']:
        languages[chat_id] = data['social']['language']
        languages_chosen[chat_id] = True

    return True
