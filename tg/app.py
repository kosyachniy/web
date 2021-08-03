"""
Telegram bot Endpoints (Transport level)
"""

# Libraries
## System
import json

## External
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

## Local
from funcs import api


# Params
with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    WEBHOOK_URL = sets['server']
    TG_TOKEN = sets['token']

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80


# Global variables
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


# Funcs
@dp.message_handler()
async def echo(message: types.Message):
    """ Main handler """

    social_user_id = message.chat.id
    text = message.text

    error, result = api(social_user_id, 'posts.get', {
        'search': text,
    })

    if not error:
        posts = result['posts']
        res = ("-"*15).join(f"#{post['id']} {post['name']}" for post in posts)
    else:
        res = f"{text}: {result}"

    await bot.send_message(social_user_id, res)


async def on_start():
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
