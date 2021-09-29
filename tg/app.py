"""
Telegram bot Endpoints (Transport level)
"""

import json

from funcs import api
from funcs.tg import tg


with open('sets.json', 'r', encoding='utf-8') as file:
    sets = json.loads(file.read())['tg']
    WEBHOOK_URL = sets['server']

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80


@tg.dp.message_handler()
async def echo(message: tg.types.Message):
    """ Main handler """

    chat = message.chat
    text = message.text

    error, result = await api(chat, 'posts.get', {
        'search': text,
    })

    if not error:
        posts = result['posts']
        res = "\n---------------\n".join(
            f"#{post['id']} {post['name']}"
            for post in posts
        )
    else:
        res = f"{text}: {result}"

    text = f"---\n{res}\n---"
    await tg.send(chat.id, text)


async def on_start(_):
    """ Handler on the bot start """

    await tg.set(WEBHOOK_URL)

    # # Actions after start

# async def on_stop(dp):
#     """ Handler on the bot stop """

#     # # Actions before shutdown

#     # Remove webhook (not acceptable in some cases)
#     await tg.stop()

#     # Close DB connection (if used)
#     await dp.storage.close()
#     await dp.storage.wait_closed()


if __name__ == '__main__':
    tg.start(
        dispatcher=tg.dp,
        webhook_path='',
        on_startup=on_start,
        # on_shutdown=on_stop,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
