"""
Telegram bot (Transport level)
"""

from aiogram.types import BotCommand

# pylint: disable=wildcard-import,unused-wildcard-import
from handlers.menu import *
from handlers.posts import *
from handlers.main import *
from handlers.media import *
from lib import cfg, report
from lib.tg import tg
from lib.queue import get, save
# from middlewares.get_variables import VariablesMiddleware


@tg.dp.errors_handler()
async def handle_errors(update, error):
    """ Exception handler """

    if 'callback_query' in update:
        chat_id = update['callback_query']['message']['chat']['id']
    else:
        chat_id = update['message']['chat']['id']

    cache = get(chat_id, {})
    await report.critical("Bot error", {
        'chat_id': chat_id,
        **cache,
    }, error=error)

    message_id = await tg.send(
        chat_id,
        "Бот умер 😵‍💫\nМеня уже лечат!",
        buttons=[{'name': 'Мои посты', 'data': 'menu'}],
    )
    cache['m'] = message_id
    save(chat_id, cache)

    return True


async def on_start(_):
    """ Handler on the bot start """
    await tg.set(cfg('tg'))
    await tg.dp.bot.set_my_commands([
        BotCommand(command='start', description="Перезапустить бота"),
        BotCommand(command='menu', description="Мои посты"),
        BotCommand(command='profile', description="Профиль"),
        BotCommand(command='help', description="Об экосистеме"),
    ])

# async def on_stop(dp):
#     """ Handler on the bot stop """

#     # # Actions before shutdown

#     # Remove webhook (not acceptable in some cases)
#     await tg.stop()

#     # Close DB connection (if used)
#     await dp.storage.close()
#     await dp.storage.wait_closed()


if __name__ == '__main__':
    # tg.dp.middleware.setup(VariablesMiddleware())
    # register_menu(tg.dp)
    tg.start(
        dispatcher=tg.dp,
        webhook_path='',
        on_startup=on_start,
        # on_shutdown=on_stop,
        skip_updates=True,
        host='0.0.0.0',
        port=80,
    )
