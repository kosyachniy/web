"""
API functionality for the Telegram bot
"""

import io
import json
import time

import requests
from libdev.cfg import cfg

# pylint: disable=import-error
from lib._variables import (
    locales, locales_chosen, tokens,
    user_ids, user_logins, user_statuses, user_names, user_titles,
)
from lib.reports import report


LOG_LIMIT = 330


async def api(chat, method, data=None, locale=None, force=False):
    """ API request """

    if not force and chat.id not in tokens:
        res = await auth(chat)

        if res is None:
            return 1, None

    if data is None:
        data = {}

    headers = {
        'accept-language': locale or locales.get(chat.id, cfg('locale')),
    }
    if chat.id in tokens:
        headers['Authorization'] = f'Bearer {tokens[chat.id]}'

    # TODO: rm
    await report.debug("API request", {
        'user': chat.id,
        'method': method,
        'data': json.dumps(data, ensure_ascii=False)[:LOG_LIMIT],
        'headers': headers,
    })

    # TODO: Rewrite `while True` & `time.sleep`
    while True:
        res = requests.post(
            cfg('api') + method.replace('.', '/') + ('/' if method else ''),
            json=data,
            headers=headers,
            timeout=60,
        )

        if int(res.status_code) != 502:
            break

        time.sleep(5)

    if int(res.status_code) >= 500:
        await report.error("API response", {
            'user': chat.id,
            'method': method,
            'params': data,
            'token': tokens.get(chat.id),
            'locale': locales.get(chat.id),
            'error': res.status_code,
        })
        return 1, None

    try:
        data = res.json()
    except requests.exceptions.JSONDecodeError:
        data = res.text

    # TODO: rm
    await report.debug("API response", {
        'user': chat.id,
        'status': res.status_code,
        'data': data,
    })

    return int(res.status_code), data

async def auth(chat, utm=None, locale=None, image=None) -> bool:
    """ User authentication """

    if chat.id in tokens:
        return False

    # Get token
    error, data = await api(chat, 'account.token', {
        'token': f'tg{chat.id}',
        'network': 'tg',
        'utm': utm,
    }, locale=locale, force=True)

    if error != 200:
        return

    tokens[chat.id] = data['token']

    if chat.id in user_ids:
        return False

    # Default settings
    if chat.id not in locales:
        locales[chat.id] = locale or cfg('locale')

    # Auth
    error, data = await api(chat, 'account.bot', {
        'user': chat.id,
        'name': chat.first_name or chat.title or None,
        'surname': chat.last_name or None,
        'login': chat.username or None,
        'utm': utm,
    }, locale=locale)

    if error != 200:
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

    # Update global variables
    tokens[chat.id] = data['token']
    user_ids[chat.id] = data['id']
    user_logins[chat.id] = data.get('login')
    user_names[chat.id] = data.get('name', '')
    user_titles[chat.id] = data.get('title', '')
    user_statuses[chat.id] = data.get('status', 3)
    if 'locale' in data['social']:
        locales[chat.id] = data['social']['locale']
        locales_chosen[chat.id] = True

    # Saving the avatar
    if image and (data.get('new') or not data.get('image')):
        image = (await image).photos or None
        if image:
            file = io.BytesIO()
            await image[0][-1].download(destination_file=file)
            image = await upload(chat, file.read())
            await api(chat, 'account.save', {
                'image': image,
            })

    return True

async def upload(chat, data):
    """ Upload image """
    return requests.post(
        f"{cfg('api')}upload/",
        files={'upload': data},
        headers={'Authorization': f'Bearer {tokens[chat.id]}'},
        timeout=30,
    ).json()['url']
