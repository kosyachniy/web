"""
Posts handler
"""

from libdev.time import get_time

from middlewares.prepare_message import prepare_message
from lib import api, cfg
from lib.tg import tg
from lib.queue import save


async def send_post(chat, post):
    """ Send formatted post """

    text = ''
    if post.get('title'):
        text += post['title'] + "\n\n"
    text += (
        "Выбери блок, который хочешь заполнить"
        ", или жми «💾 Опубликовать 💾»"
    )

    img = ['☑️', '✅'][bool(post.get('image'))]
    nam = ['☑️', '✅'][bool(post.get('title'))]
    dat = ['☑️', '✅'][bool(post.get('data'))]

    return await tg.send(chat.id, text, buttons=[[
        {'name': f'{nam} Название {nam}', 'data': 'nam'},
        {'name': f'{dat} Содержимое {dat}', 'data': 'dat'},
    ], [
        {'name': f'{img} Изображение {img}', 'data': 'img'},
    ], [
        {'name': '💾 Опубликовать 💾', 'data': 'finish'},
    ], [
        {'name': '🗑 Удалить 🗑', 'data': 'rm'},
    ]], inline=True)

async def send_posts(chat, posts=None):
    """ Send formatted list of posts """

    if posts is None:
        error, data = await api(chat, 'posts.get', {'my': True})
        if error != 200:
            return None
        posts = data['posts']

    return await tg.send(chat.id, "Мои посты", buttons=[{
        'name': post['title'],
        'data': f"res{post['id']}",
    } for post in posts] + [{
        'name': "➕ Создать пост ➕",
        'data': 'create',
    }])


@tg.dp.callback_query_handler(lambda mes: mes.data[:3] == 'res')
async def get_post(callback):
    """ Get """

    chat, text, cache = await prepare_message(callback)
    if chat is None:
        return

    if len(text) == 3:
        post_id = cache.get('p')
    else:
        post_id = int(text[3:])

    _, data = await api(chat, 'posts.get', {'id': post_id})
    message_id = await send_post(chat, data['posts'])

    save(chat.id, {
        's': 'res',
        'p': post_id,
        'm': message_id,
    })

@tg.dp.callback_query_handler(lambda mes: mes.data == 'nam')
async def edit_title(callback):
    """ Edit title """

    chat, _, cache = await prepare_message(callback)
    if chat is None:
        return

    message_id = await tg.send(chat.id, "Заголовок")

    cache['s'] = 'nam'
    cache['m'] = message_id
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'dat')
async def edit_data(callback):
    """ Edit data """

    chat, _, cache = await prepare_message(callback)
    if chat is None:
        return

    message_id = await tg.send(chat.id, "Содержимое")

    cache['s'] = 'dat'
    cache['m'] = message_id
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'img')
async def edit_image(callback):
    """ Edit image """

    chat, _, cache = await prepare_message(callback)
    if chat is None:
        return

    message_id = await tg.send(chat.id, "Отправь изображение")

    cache['s'] = 'img'
    cache['m'] = message_id
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'create')
async def create(callback):
    """ Create """

    chat, _, _ = await prepare_message(callback)
    if chat is None:
        return

    _, data = await api(chat, 'posts.save')

    message_id = await send_post(chat, data['post'])
    save(chat.id, {
        'm': message_id,
        's': 'res',
        'p': data['id'],
    })

@tg.dp.callback_query_handler(lambda mes: mes.data == 'rm')
async def delete(callback):
    """ Delete """

    chat, _, cache = await prepare_message(callback)
    if chat is None:
        return

    post_id = cache.get('p')

    _, data = await api(chat, 'posts.get', {'id': post_id})
    message_id = await tg.send(
        chat.id,
        f"Уверен, что хочешь удалить {data['posts']['title']}",
        buttons=[[{
            'name': 'Нет', 'data': 'menu',
        }, {
            'name': 'Да', 'data': 'rmy',
        }]],
        inline=True,
    )
    cache['s'] = 'rm'
    cache['m'] = message_id
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'rmy')
async def deletey(callback):
    """ Approve delete """

    chat, _, cache = await prepare_message(callback)
    if chat is None:
        return

    post_id = cache.get('p')
    await api(chat, 'posts.rm', {'id': post_id})

    cache['m'] = await send_posts(chat)
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'finish')
async def finish(callback):
    """ Finish """

    # TODO: upload_document, typing
    chat, text, cache = await prepare_message(callback, 'upload_document')
    if chat is None:
        return

    post_id = cache.get('p')
    _, data = await api(chat, 'posts.get', {'id': post_id})
    post = data['posts']

    # error, data = await api(chat, 'posts.make', {'id': post_id})
    # if error != 200:
    #     message_id = await tg.send(
    #         chat.id,
    #         "Бесплатная версия истекла",
    #         buttons=[{
    #             'name': 'Создать ещё',
    #             'data': 'create',
    #         }, {
    #             'name': 'Редактировать',
    #             'data': f'res{post_id}',
    #         }],
    #     )

    #     cache['s'] = 'limit'
    #     cache['m'] = message_id
    #     save(chat.id, cache)
    #     return

    text = f"Пост #{post['id']} «{post['title']}»"
    if post['data']:
        text += f"\n\n{post['data']}"
    text += (
        f"\n\nСоздано: {get_time(post['created'], tz=cfg('timezone'))}"
        f"\nИзменено: {get_time(post['updated'], tz=cfg('timezone'))}"
    )

    message_id = await tg.send(
        chat.id,
        text,
        files=post.get('image'),
        buttons=[{
            'name': 'Создать ещё',
            'data': 'create',
        }, {
            'name': 'Редактировать',
            'data': f'res{post_id}',
        }],
        markup=None,
    )

    cache['s'] = 'finish'
    cache['m'] = message_id
    save(chat.id, cache)
