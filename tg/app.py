"""
Telegram bot (Transport level)
"""

from libdev.codes import get_flag

from lib import (
    auth, api, cfg, report,
    languages, user_ids, user_logins, user_statuses, user_titles,
)
from lib.tg import tg


WEBHOOK_URL = cfg('tg.server')
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80
BUTTONS = [
    ['Профиль', 'Настройки'],
]


async def check_user(chat, public=False):
    """ Authorize user and check access """

    res = await auth(chat)

    if res is None:
        await tg.send(
            chat.id,
            "Бот обновляется 😵‍💫\nУже скоро смогу ответить!",
            buttons=BUTTONS,
        )
        await report.error("Check user", {'user': chat.id})
        return True

    if not public and user_statuses[chat.id] < 4:
        await tg.send(chat.id, "Нет доступа 😛", buttons=BUTTONS)
        await report.important("Несанкционированный доступ", {
            'user': user_ids[chat.id],
            'name': user_titles[chat.id],
            'social_user': chat.id,
            'social_login': user_logins[chat.id],
            'status': user_statuses[chat.id],
        })
        return True

def get_user(chat_id):
    """ Get user info """

    text = f"{get_flag(languages[chat_id])} {user_titles[chat_id]}"
    if user_logins[chat_id]:
        text += f" (@{user_logins[chat_id]})"

    return text


@tg.dp.message_handler(commands=['start', 'help', 'info', 'about'])
async def start(message):
    """ Start handler """

    chat = message.chat

    if await check_user(chat, True):
        return

    await tg.send(
        chat.id,
        f"Вы авторизованы как {get_user(chat.id)}",
        buttons=BUTTONS,
    )

@tg.dp.message_handler(lambda msg: msg.text.lower() == 'профиль')
async def profile(message):
    """ Profile """

    chat = message.chat

    if await check_user(chat, True):
        return

    await tg.send(chat.id, get_user(chat.id), buttons=BUTTONS)

@tg.dp.message_handler()
async def echo(message):
    """ Main handler """

    chat = message.chat
    text = message.text

    error, data = await api(chat, 'posts.get', {
        'search': text,
    })

    if not error:
        posts = data['posts']
        res = "\n---------------\n".join(
            f"#{post['id']} {post['name']}"
            for post in posts
        )
    else:
        res = f"{text}: {data}"

    text = f"---\n{res}\n---"
    await tg.send(chat.id, text, buttons=BUTTONS)


async def on_start(_):
    """ Handler on the bot start """
    await tg.set(WEBHOOK_URL)

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
