"""
API functionality for the Telegram bot
"""

# Libraries
## System
import json
import time

## External
import requests

## Local
from ._variables import languages, languages_chosen, tokens, ids
from ._generate import generate
from ._reports import report


# Params
with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    SERVER_LINK = sets['server']

LOG_LIMIT = 330


# Funcs
async def api(social_user, method, data=None):
    """ API request """

    social_user_id = social_user.id

    if data is None:
        data = {}

    if social_user_id not in tokens:
        res = await auth(social_user)

        # TODO: social auth
        # if res is None:
        #     return 1, None

    req = {
        'method': method,
        'params': data,
        'token': tokens[social_user_id],
        'network': 'tg',
        'locale': languages[social_user_id],
    }

    await report.debug(
        "API request",
        {
            'user': social_user_id,
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
                'user': social_user_id,
                'method': method,
                'params': data,
                'token': tokens[social_user_id],
                'locale': languages[social_user_id],
                'error': res.status_code,
            }
        )
        return 1, None

    res = res.json()

    await report.debug(
        "API response",
        {
            'user': social_user_id,
            'data': res,
        }
    )

    return res['error'], res['result']

async def auth(social_user) -> bool:
    """ User authentication """

    social_user_id = social_user.id

    if social_user_id in ids:
        return False

    # Default settings
    if social_user_id not in languages:
        languages[social_user_id] = 1 # TODO: 0

    ## Token
    token = generate()
    tokens[social_user_id] = token

    ## Call the API
    error, result = await api(social_user, 'account.bot', {
        'user': social_user.id,
        'name': social_user.first_name or None,
        'surname': social_user.last_name or None,
        'login': social_user.username or None,
    })

    # Errors
    if error:
        await report.error(
            "Authorization",
            {
                'user': social_user.id,
                'name': social_user.first_name or None,
                'surname': social_user.last_name or None,
                'login': social_user.username or None,
                'error': error,
                'result': result,
            }
        )
        return

    ## Update global variables

    ids[social_user_id] = result['id']

    if 'language' in result['social']:
        languages[social_user_id] = result['social']['language']
        languages_chosen[social_user_id] = True

    return True
