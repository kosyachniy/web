"""
Bot commands handler
"""

import jwt

from middlewares.prepare_message import prepare_message
from handlers.main import get_user
from handlers.posts import send_posts
from lib import cfg
from lib.tg import tg
from lib.queue import save


@tg.dp.message_handler(commands=['menu'])
async def handler_menu_command(message):
    """ Menu handler """

    chat, _, cache = await prepare_message(message)
    if chat is None:
        return

    cache['m'] = await send_posts(chat)
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'menu')
async def handler_menu_callback(message):
    """ Menu handler """

    chat, _, cache = await prepare_message(message)
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

@tg.dp.message_handler(commands=['profile'])
async def handler_profile_command(message):
    """ Profile """

    chat, _, _ = await prepare_message(message)
    if chat is None:
        return

    code = jwt.encode({
        'user': chat.id,
    }, cfg('jwt'), algorithm='HS256')

    message_id = await tg.send(chat.id, (
        f"Ты авторизован как {get_user(chat.id)}"
    ), buttons=[{
        'name': 'Открыть профиль',
        'data': f"{cfg('web')}callback/telegram?code={code}",
    }])
    save(chat.id, {'m': message_id})

@tg.dp.callback_query_handler(lambda mes: mes.data == 'profile')
async def handler_profile_callback(message):
    """ Profile """

    chat, _, _ = await prepare_message(message)
    if chat is None:
        return

    code = jwt.encode({
        'user': chat.id,
    }, cfg('jwt'), algorithm='HS256')

    message_id = await tg.send(chat.id, (
        f"Ты авторизован как {get_user(chat.id)}"
    ), buttons=[{
        'name': 'Открыть профиль',
        'data': f"{cfg('web')}callback/telegram?code={code}",
    }])
    save(chat.id, {'m': message_id})

@tg.dp.message_handler(lambda msg: msg.text.lower() == 'профиль')
async def handler_profile_text(message):
    """ Profile """

    chat, _, _ = await prepare_message(message)
    if chat is None:
        return

    code = jwt.encode({
        'user': chat.id,
    }, cfg('jwt'), algorithm='HS256')

    message_id = await tg.send(chat.id, (
        f"Ты авторизован как {get_user(chat.id)}"
    ), buttons=[{
        'name': 'Открыть профиль',
        'data': f"{cfg('web')}callback/telegram?code={code}",
    }])
    save(chat.id, {'m': message_id})


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
