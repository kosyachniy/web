"""
Telegram bot (Transport level)
"""

from libdev.codes import get_flag
from libdev.doc import to_base64

from lib import (
    auth, api, cfg, report,
    languages, user_ids, user_logins, user_statuses, user_titles,
)
from lib.tg import tg
from lib.queue import save, get


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
        login = user_logins[chat_id].replace('_', '\\_')
        text += f" (@{login})"

    return text

async def send_posts(chat, posts=None):
    """ Send posts """

async def send_post(chat, post):
    """ Send post """


@tg.dp.message_handler(commands=['start'])
async def start(message):
    """ Start handler """

    chat = message.chat
    cache = get(chat.id, {})

    if cache.get('m'):
        await tg.rm(chat.id, cache['m'])
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    post_id = cache.get('p')

    # Unfinished
    if post_id:
        _, data = await api(chat, 'posts.get', {'id': post_id})
        message_id = await send_post(chat, data['posts'])
        cache['m'] = message_id
        cache['s'] = 'res'
        save(chat.id, cache)
        return

    # List
    _, data = await api(chat, 'posts.get')
    if len(data['posts']):
        message_id = await send_posts(chat, data['posts'])
        cache['m'] = message_id
        cache['s'] = 'res'
        save(chat.id, cache)
        return

    # New
    messages = []

    text = "Хай 🌴"
    messages.extend(await tg.send(chat.id, text))

    _, data = await api(chat, 'posts.save')

    messages.extend(await send_post(chat, data['post']))
    save(chat.id, {
        'm': messages,
        's': 'res',
        'p': data['id'],
    })

@tg.dp.message_handler(commands=['help', 'info', 'about'])
async def info(message):
    """ Info handler """

    chat = message.chat
    cache = get(chat.id, {})

    if cache.get('m'):
        await tg.rm(chat.id, cache['m'])
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    message_id = await tg.send(chat.id, (
        f"Ты авторизован как {get_user(chat.id)}"
        f"\n\nDev Bot — это проект экосистемы Chill.Services"
        f"\nСделано [Алексей Полоз](https://t.me/kosyachniy)"
        f"\n\n🛟 Пиши по любым вопросам, проблемам и предложениям"
    ), buttons=BUTTONS)
    save(chat.id, {'m': message_id})

@tg.dp.message_handler(commands=['menu'])
# @tg.dp.callback_query_handler(lambda mes: mes.data == 'menu')
# @tg.dp.message_handler(lambda msg: msg.text.lower() == 'menu')
async def menu(message):
    """ Menu handler """

    chat = message.chat
    cache = get(chat.id, {})

    if cache.get('m'):
        await tg.rm(chat.id, cache['m'])
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    await send_posts(chat)

@tg.dp.message_handler(lambda msg: msg.text.lower() == 'profile')
async def profile(message):
    """ Profile """

    chat = message.chat
    cache = get(chat.id, {})

    if cache.get('m'):
        await tg.rm(chat.id, cache['m'])
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    message_id = await tg.send(chat.id, (
        f"Ты авторизован как {get_user(chat.id)}"
        f"\nПерейти в профиль →"
    ), buttons=BUTTONS)
    save(chat.id, {'m': message_id})

@tg.dp.message_handler()
async def echo(message):
    """ Main handler """

    chat = message.chat
    text = message.text
    cache = get(chat.id, {})

    if cache.get('m'):
        await tg.rm(chat.id, cache['m'])
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    if cache.get('s') == 'post':
        await tg.send(chat.id, text, buttons=BUTTONS)
    else:
        await report.important("Feedback", {
            'text': text,
            'cache': cache,
        })

        text = "Передал твой фидбек!"
        message_id = await tg.send(chat.id, text, buttons=BUTTONS)
        cache['m'] = message_id
        save(chat.id, cache)

@tg.dp.message_handler(content_types=['photo'])
async def handle_photo(message):
    """ Photo handler """

    chat = message.chat
    photo = await tg.bot.download_file(
        (await tg.bot.get_file(
            message.photo[-1].file_id
        )).file_path
    )
    text = message.caption or ''
    cache = get(chat.id, {})

    if cache.get('m'):
        await tg.rm(chat.id, cache['m'])
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    if cache.get('s') == 'img':
        error, data = await api(chat, 'posts.save', {
            'id': cache.get('p'),
            'img': to_base64(photo),
        })
        if error:
            text = "Неверный формат, попробуй ещё раз"
            message_id = await tg.send(chat.id, text)
        else:
            message_id = await send_post(chat, data['posts'])
            cache['s'] = 'res'
        cache['m'] = message_id
        save(chat.id, cache)

    else:
        # TODO: docs via report
        # await report.important("Feedback", {
        #     'text': text,
        #     'cache': cache,
        # })

        await tg.forward(cfg('bug_chat'), chat.id, message.message_id)

        text = "Передал твой фидбек!"
        message_id = await tg.send(chat.id, text, buttons=BUTTONS)
        cache['m'] = message_id
        save(chat.id, cache)

@tg.dp.message_handler(content_types=['document'])
async def handle_doc(message):
    """ Document handler """

    chat = message.chat
    mime = message.document.mime_type
    photo = await tg.bot.download_file(
        (await tg.bot.get_file(
            message.document.file_id
        )).file_path
    )
    text = message.caption or ''
    cache = get(chat.id, {})

    if cache.get('m'):
        await tg.rm(chat.id, cache['m'])
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    if cache.get('s') == 'img':
        try:
            photo = to_base64(photo, mime)
        # pylint: disable=broad-except
        except Exception as e:
            await tg.send(chat.id, "Неверный формат, попробуй ещё раз")
            print(e, type(e))

        error, data = await api(chat, 'posts.save', {
            'id': cache.get('p'),
            'img': photo,
        })
        if error:
            text = "Неверный формат, попробуй ещё раз"
            message_id = await tg.send(chat.id, text)
        else:
            message_id = await send_post(chat, data['posts'])
            cache['s'] = 'res'
        cache['m'] = message_id
        save(chat.id, cache)

    else:
        # TODO: docs via report
        # await report.important("Feedback", {
        #     'text': text,
        #     'cache': cache,
        # })

        await tg.forward(cfg('bug_chat'), chat.id, message.message_id)

        text = "Передал твой фидбек!"
        message_id = await tg.send(chat.id, text, buttons=BUTTONS)
        cache['m'] = message_id
        save(chat.id, cache)


async def on_start(_):
    """ Handler on the bot start """
    await tg.set(cfg('tg'))

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
        host='0.0.0.0',
        port=80,
    )
