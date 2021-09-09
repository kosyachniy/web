"""
Telegram bot Endpoints (Transport level)
"""

# Libraries
## System
import json

## External
from aiogram import types
from aiogram.utils.executor import start_webhook

## Local
from funcs import api
from funcs.tg import bot, dp, send


# Params
with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    WEBHOOK_URL = sets['server']
    TG_TOKEN = sets['token']

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80


# Funcs
@dp.message_handler()
async def echo(message: types.Message):
    """ Main handler """

    social_user = message.from_user
    text = message.text

    error, result = await api(social_user, 'posts.get', {
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
    await send(social_user.id, text)


async def on_start(dp):
    """ Handler on the bot start """

    await bot.set_webhook(WEBHOOK_URL)

    # # Actions after start

# async def on_stop(dp):
#     """ Handler on the bot stop """

#     # # Actions before shutdown

#     # Remove webhook (not acceptable in some cases)
#     await bot.delete_webhook()

#     # Close DB connection (if used)
#     await dp.storage.close()
#     await dp.storage.wait_closed()


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_start,
        # on_shutdown=on_stop,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
