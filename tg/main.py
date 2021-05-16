# Libraries
## System
import json
import logging

## External
from aiogram import Bot, types
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook


# Params
with open('sets.json', 'r') as file:
	sets = json.loads(file.read())
	print(sets)
	WEBHOOK_URL = sets['tg']['server']

with open('keys.json', 'r') as file:
	keys = json.loads(file.read())
	print(keys)
	TG_TOKEN = keys['tg']['token']

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80


# Global variables
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)
# dp.middleware.setup(LoggingMiddleware())


# Funcs
@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start

async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )