from libdev.time import get_time

from lib import api, cfg
from lib.tg import tg
from lib.queue import save
from middlewares.prepare_message import prepare_message


async def send_post(chat, post):
    text = ''
    if post.get('pos'):
        text += post.get('title', '') + "\n\n"
    text += (
        "Выбери блок, который хочешь заполнить"
        ", или жми «Сохранить пост»"
    )

    img = ['☑️', '✅'][bool(post.get('img'))]
    fio = ['☑️', '✅'][bool(post.get('fio'))]
    pos = ['☑️', '✅'][bool(post.get('pos'))]
    age = ['☑️', '✅'][bool(post.get('birth'))]
    geo = ['☑️', '✅'][bool(post.get('geo'))]
    cont = ['☑️', '✅'][bool(post.get('phone') or post.get('mail'))]
    job = ['☑️', '✅'][bool(post.get('job'))]
    edu = ['☑️', '✅'][bool(post.get('edu'))]
    cours = ['☑️', '✅'][bool(post.get('cours'))]
    skill = ['☑️', '✅'][bool(post.get('skill'))]
    lang = ['☑️', '✅'][bool(post.get('lang'))]
    conf = ['☑️', '✅'][bool(post.get('conf'))]
    comp = ['☑️', '✅'][bool(post.get('comp'))]
    proj = ['☑️', '✅'][bool(post.get('proj'))]

    return await tg.send(chat.id, text, buttons=[[
        {'name': f'{pos} Должность {pos}', 'data': 'pos'},
        {'name': f'{fio} ФИО {fio}', 'data': 'fio'},
    ], [
        {'name': f'{img} Фото {img}', 'data': 'img'},
        {'name': f'{age} Возраст {age}', 'data': 'age'},
    ], [
        {'name': f'{geo} Город {geo}', 'data': 'geo'},
        {'name': f'{cont} Контакты {cont}', 'data': 'cont'},
    ], [
        {'name': f'{job} Опыт работы {job}', 'data': 'job'},
        {'name': f'{proj} Проекты {proj}', 'data': 'proj'},
    ], [
        {'name': f'{edu} Образование {edu}', 'data': 'edu'},
        {'name': f'{cours} Курсы {cours}', 'data': 'cour'},
    ], [
        {'name': f'{skill} Навыки {skill}', 'data': 'skill'},
        {'name': f'{lang} Языки {lang}', 'data': 'lang'},
    ], [
        {'name': f'{conf} Конференции {conf}', 'data': 'conf'},
        {'name': f'{comp} Соревнования {comp}', 'data': 'comp'},
    ], [
        {'name': 'Сгенерировать PDF', 'data': 'finish'},
    ], [
        {'name': '🗑 Удалить 🗑', 'data': 'rm'},
    ]], inline=True)

async def send_posts(chat, posts=None):
    if posts is None:
        error, data = await api(chat, 'posts.get')
        if error:
            return None
        posts = data['posts']

    return await tg.send(chat.id, "Мои посты", buttons=[{
        'name': post['title'],
        'data': f"res{post['id']}",
    } for post in posts] + [{
        'name': "Создать пост",
        'data': 'create',
    }])


@tg.dp.callback_query_handler(lambda mes: mes.data[:3] == 'res')
async def post(callback):
    """ Get post """

    chat, text, cache = await prepare_message(callback)
    if chat is None:
        return

    if len(text) == 3:
        post_id = cache.get('p')
    else:
        post_id = int(text[3:])

    error, data = await api(chat, 'posts.get', {'id': post_id})
    message_id = await send_post(chat, data['posts'])

    save(chat.id, {
        's': 'res',
        'p': post_id,
        'm': message_id,
    })

@tg.dp.callback_query_handler(lambda mes: mes.data == 'pos')
async def position(callback):
    """ Edit position """

    chat, text, cache = await prepare_message(callback)
    if chat is None:
        return

    message_id = await tg.send(chat.id, (
        "Желаемая позиция"
        "\n\n_например: «контент-менеджер», «графический дизайнер»_"
    ))

    cache['s'] = 'pos'
    cache['m'] = message_id
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'create')
async def create(callback):
    """ Create post """

    chat, text, cache = await prepare_message(callback)
    if chat is None:
        return

    error, data = await api(chat, 'posts.save')

    message_id = await send_post(chat, data['post'])
    save(chat.id, {
        'm': message_id,
        's': 'res',
        'p': data['id'],
    })

@tg.dp.callback_query_handler(lambda mes: mes.data == 'rm')
async def delete(callback):
    """ Delete post """

    chat, text, cache = await prepare_message(callback)
    if chat is None:
        return

    post_id = cache.get('p')

    error, data = await api(chat, 'posts.get', {'id': post_id})
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
    """ Approve delete post """

    chat, text, cache = await prepare_message(callback)
    if chat is None:
        return

    post_id = cache.get('p')
    error, data = await api(chat, 'posts.rm', {'id': post_id})

    cache['m'] = await send_posts(chat)
    save(chat.id, cache)

@tg.dp.callback_query_handler(lambda mes: mes.data == 'finish')
async def finish(callback):
    """ Finish """

    chat, text, cache = await prepare_message(callback, 'upload_document')
    if chat is None:
        return

    post_id = cache.get('p')
    # error, data = await api(chat, 'posts.get', {'id': post_id})
    # post = data['posts']

    error, data = await api(chat, 'posts.make', {'id': post_id})
    if error:
        message_id = await tg.send(chat.id, "Бесплатная версия истекла", buttons=[{
            'name': 'Создать ещё',
            'data': 'create',
        }, {
            'name': 'Редактировать',
            'data': f'res{post_id}',
        }])

        cache['s'] = 'limit'
        cache['m'] = message_id
        save(chat.id, cache)
        return

    text = "✨ происходит магия ✨"

    # text = f"Пост #{post['id']} {post['title']}"
    # if post['fio']:
    #     text += f"\n{post['fio']}"
    # if post.get('birth'):
    #     if not post['fio']:
    #         text += "\n"
    #     else:
    #         text += " ("
    #     text += f"{get_time(post['birth'], '%d.%m.%Y', cfg('timezone'))}"
    #     if post['fio']:
    #         text += ")"
    # if post.get('pos'):
    #     text += f"\n{post['pos']}"
    # if post.get('geo'):
    #     if not post['pos']:
    #         text += "\n"
    #     else:
    #         text += " ("
    #     text += f"{post['geo']}"
    #     if post['pos']:
    #         text += ")"
    # if post.get('phone') or post.get('mail'):
    #     text += "\n"
    #     if post.get('phone'):
    #         text += f"{post['phone']}"
    #         if post.get('mail'):
    #             text += " / "
    #     if post.get('mail'):
    #         text += f"{post['mail']}"

    # img = None
    # if post.get('img'):
    #     img = f"http://cv.chill.services/load/{post['img']}"

    message_id = await tg.send(chat.id, text, buttons=[{ # files=img,
        'name': 'Создать ещё',
        'data': 'create',
    }, {
        'name': 'Редактировать',
        'data': f'res{post_id}',
    }], markup=None)

    cache['s'] = 'finish'
    cache['m'] = message_id
    save(chat.id, cache)
