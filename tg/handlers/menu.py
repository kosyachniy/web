"""
Bot commands handler
"""

from lib.tg import tg
from lib.queue import save
from middlewares.prepare_message import prepare_message
from handlers.posts import send_posts


@tg.dp.message_handler(commands=['menu'])
async def handler_menu_command(message):
    """ Menu handler """

    chat, _, cache = await prepare_message(message)
    if chat is None:
        return

    cache['m'] = await send_posts(chat)
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'menu')
async def handler_menu_callback(callback):
    """ Menu handler """

    chat, _, cache = await prepare_message(callback)
    if chat is None:
        return

    cache['m'] = await send_posts(chat)
    save(chat.id, cache)

@tg.dp.message_handler(lambda msg: msg.text.lower() == 'мои посты')
async def handler_menu_text(message):
    """ Menu handler """

    chat, _, cache = await prepare_message(message)
    if chat is None:
        return

    cache['m'] = await send_posts(chat)
    save(chat.id, cache)


# def register_menu(dp):
#     dp.register_message_handler(
#         menu,
#         commands=['menu'],
#     )
#     dp.register_message_handler(
#         menu,
#         lambda mes: mes.data == 'menu',
#     )
#     dp.register_message_handler(
#         menu,
#         lambda msg: msg.text.lower() == 'мои посты',
#     )
