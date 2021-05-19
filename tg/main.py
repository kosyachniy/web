# Libraries
## System
import json

## External
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook


# Params
with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    WEBHOOK_URL = sets['tg']['server']

with open('keys.json', 'r') as file:
    keys = json.loads(file.read())
    TG_TOKEN = keys['tg']['token']

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80


# Global variables
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


# Funcs
@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


async def on_start(dp):
    await bot.set_webhook(WEBHOOK_URL)

    # # Actions after start

# async def on_stop(dp):
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