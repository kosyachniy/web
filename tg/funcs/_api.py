"""
API functionality for the Telegram bot
"""

# Libraries
## System
import json

## External
import requests

## Local
from funcs import languages, tokens


# Params
with open('sets.json', 'r') as file:
	sets = json.loads(file.read())
	SERVER_LINK = sets['server']

LOG_LIMIT = 330


# Funcs
def api(social_user_id, method, data=None):
    """ API request """

    if data is None:
        data = {}

    # Default settings
    if social_user_id not in languages:
        languages[social_user_id] = 1 # TODO: 0

    req = {
        'method': method,
        'params': data,
        'token': tokens[social_user_id],
        'network': 2,
        'language': languages[social_user_id],
    }

    print(
        f"req\t{social_user_id}"
        f"\t{json.dumps(req, ensure_ascii=False)[:LOG_LIMIT]}"
    )

    res = requests.post(SERVER_LINK, json=req).json()

    print(f"res\t{social_user_id}\t{res}")

    return res['error'], res['result']
