"""
API functionality for the Telegram bot
"""

import json
import time

import requests
from libdev.cfg import cfg
from libdev.gen import generate

from lib._variables import (
    locales, locales_chosen, tokens,
    user_ids, user_logins, user_statuses, user_names, user_titles,
)
from lib.reports import report


LOG_LIMIT = 330


async def api(chat, method, data=None):
    """ API request """

    if data is None:
        data = {}

    if chat.id not in tokens:
        res = await auth(chat)

        if res is None:
            return 1, None

    req = {
        'method': method,
        'params': data,
        'token': tokens[chat.id],
        'network': 'tg',
        'locale': locales[chat.id],
    }

    await report.debug("API request", {
        'user': chat.id,
        'data': json.dumps(req, ensure_ascii=False)[:LOG_LIMIT],
    })

    # TODO: Rewrite `while True` & `time.sleep`
    while True:
        res = requests.post(cfg('api'), json=req, timeout=60)

        if res.status_code != 502:
            break

        time.sleep(5)

    if res.status_code != 200:
        await report.error("API response", {
            'user': chat.id,
            'method': method,
            'params': data,
            'token': tokens[chat.id],
            'locale': locales[chat.id],
            'error': res.status_code,
        })
        return 1, None

    res = res.json()

    await report.debug("API response", {
        'user': chat.id,
        'data': res,
    })

    return res['error'], res.get('data', {})

async def auth(chat, utm=None) -> bool:
    """ User authentication """

    if chat.id in user_ids:
        return False

    # Default settings
    if chat.id not in locales:
        locales[chat.id] = 1 # TODO: 0

    ## Token
    token = generate()
    tokens[chat.id] = token

    ## Call the API
    error, data = await api(chat, 'account.bot', {
        'user': chat.id,
        'name': chat.first_name or chat.title or None,
        'surname': chat.last_name or None,
        'login': chat.username or None,
        'utm': utm,
    })

    # Errors
    if error:
        await report.error("Authorization", {
            'user': chat.id,
            'name': chat.first_name or chat.title or None,
            'surname': chat.last_name or None,
            'login': chat.username or None,
            'error': error,
            'data': data,
        })

        del tokens[chat.id]
        return

    ## Update global variables
    user_ids[chat.id] = data['id']
    user_logins[chat.id] = data.get('login')
    user_names[chat.id] = data.get('name', '')
    user_titles[chat.id] = data.get('title', '')
    user_statuses[chat.id] = data.get('status', 3)
    if 'locale' in data['social']:
        locales[chat.id] = data['social']['locale']
        locales_chosen[chat.id] = True

    return True
