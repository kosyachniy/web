"""
Telegram bot (Transport level)
"""

from lib import (
    auth, api, cfg,
    user_logins, user_titles,
)
from lib.tg import tg


WEBHOOK_URL = cfg('tg.server')
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80
BUTTONS = [
    ['Профиль', 'Настройки'],
]


@tg.dp.message_handler(commands=['start', 'help', 'info', 'about'])
async def start(message: tg.types.Message):
    """ Start handler """

    chat = message.chat
    res = await auth(chat)

    if not res:
        await tg.send(chat.id, "Бот обновляется 😵‍💫\nУже скоро смогу ответить!")
        return

    text = f"Вы авторизованы как {user_titles[chat.id]}"
    if user_logins[chat.id]:
        text += f" (@{user_logins[chat.id]})"

    await tg.send(chat.id, text, buttons=BUTTONS)

@tg.dp.message_handler()
async def echo(message: tg.types.Message):
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
