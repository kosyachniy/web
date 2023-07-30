"""
Main commands handler
"""

import jwt
from libdev.codes import get_flag

from middlewares.prepare_message import prepare_message
from handlers.posts import send_post, send_posts
from lib import api, cfg, report, locales, user_logins, user_titles
from lib.tg import tg
from lib.queue import save


def get_user(chat_id):
    """ Get user info """

    text = f"{get_flag(locales[chat_id])} {user_titles[chat_id]}"
    if user_logins[chat_id]:
        login = user_logins[chat_id].replace('_', '\\_')
        text += f" (@{login})"

    return text


@tg.dp.message_handler(commands=['start'])
async def start(message):
    """ Start handler """

    chat, text, cache = await prepare_message(message)
    if chat is None:
        return

    if text and ' ' in text and text.split()[1] == 'auth':
        code = jwt.encode({
            'user': chat.id,
        }, cfg('jwt'), algorithm='HS256')

        await tg.send(chat.id, "Для авторизации на сайте, жми:", buttons=[{
            'name': 'Открыть',
            'data': f"{cfg('web')}callback?code={code}&social=telegram",
        }])
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
    _, data = await api(chat, 'posts.get', {'my': True})
    if len(data['posts']):
        message_id = await send_posts(chat, data['posts'])
        cache['m'] = message_id
        cache['s'] = 'res'
        save(chat.id, cache)
        return

    # New user
    messages = []

    text = "Хай! Я помогу тебе 🌴"
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

    chat, _, cache = await prepare_message(message)
    if chat is None:
        return

    cache['m'] = await tg.send(chat.id, (
        f"Ты авторизован как {get_user(chat.id)}" # TODO: link to profile
        f"\n\n{cfg('name')} — это проект экосистемы"
        f" [chill](https://chill.services/)"
        f"\nСделано [Алексей Полоз](https://t.me/kosyachniy)" # TODO: to .env
        f"\n\n🛟 Пиши по любым вопросам, проблемам и предложениям"
    ), buttons=[{
        'name': 'Меню', 'data': 'menu',
    }, {
        'name': 'Профиль', 'data': 'profile',
    }])
    save(chat.id, cache)

@tg.dp.message_handler()
async def echo(message):
    """ Main handler """

    # TODO: move sub functions to individual handlers

    chat, text, cache = await prepare_message(message)
    if chat is None:
        return

    if cache.get('s') == 'nam':
        error, data = await api(chat, 'posts.save', {
            'id': cache.get('p'),
            'title': text,
        })
        if error != 200:
            message_id = await tg.send(
                chat.id,
                "Неверный формат, попробуй ещё раз",
                buttons=[{
                    'name': 'К посту', 'data': 'res',
                }],
            )
        else:
            message_id = await send_post(chat, data['post'])
            cache['s'] = 'res'
        cache['m'] = message_id
        save(chat.id, cache)
        return

    if cache.get('s') == 'dat':
        error, data = await api(chat, 'posts.save', {
            'id': cache.get('p'),
            'data': text,
        })
        if error != 200:
            message_id = await tg.send(
                chat.id,
                "Неверный формат, попробуй ещё раз",
                buttons=[{
                    'name': 'К посту', 'data': 'res',
                }],
            )
        else:
            message_id = await send_post(chat, data['post'])
            cache['s'] = 'res'
        cache['m'] = message_id
        save(chat.id, cache)
        return

    await report.important("Feedback", {
        'text': text,
        **cache,
    })
    await tg.forward(cfg('bug_chat'), chat.id, message.message_id)

    text = "Передал твой фидбек!"
    message_id = await tg.send(
        chat.id,
        text,
        buttons=[{'name': 'Мои посты', 'data': 'menu'}],
    )
    cache['m'] = message_id
    save(chat.id, cache)
