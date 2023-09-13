"""
Media handler
"""

import io

from middlewares.prepare_message import rm_last
from middlewares.check_user import check_user
from handlers.posts import send_post
from lib import api, upload, cfg, report
from lib.tg import tg
from lib.queue import save, get


@tg.dp.message_handler(content_types=['photo'])
async def handle_photo(message):
    """ Photo handler """

    chat = message.chat
    if chat.id < 0:
        return

    image = io.BytesIO()
    await message.photo[-1].download(destination_file=image)
    text = message.caption or ''
    cache = get(chat.id, {})

    await rm_last(chat, cache)
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    if cache.get('s') == 'img':
        image = await upload(chat, image.read())
        error, data = await api(chat, 'posts.save', {
            'id': cache.get('p'),
            'image': image,
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

    else:
        await report.important("Feedback", {
            'text': 'Photo',
            **cache,
        })
        await tg.forward(cfg('bug_chat'), chat.id, message.message_id)

        text = "Передал твой запрос!"
        message_id = await tg.send(
            chat.id,
            text,
            buttons=[{'name': 'Мои посты', 'data': 'menu'}],
        )
        cache['m'] = message_id
        save(chat.id, cache)

@tg.dp.message_handler(content_types=['location'])
async def process_location(message):
    """ Location handler """

    chat = message.chat
    if chat.id < 0:
        return

    lat = message.location.latitude
    lon = message.location.longitude

    cache = get(chat.id, {})

    await rm_last(chat, cache)
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    message_id = await tg.send(
        chat.id,
        f"Широта: {lat}\nДолгота: {lon}",
    )
    # await tg.bot.send_location(chat.id, lat, lon)
    cache['m'] = message_id
    save(chat.id, cache)

@tg.dp.message_handler(content_types=['any'])
async def handle_doc(message):
    """ Document handler """

    chat = message.chat
    if chat.id < 0:
        return

    try:
        mime = message.document.mime_type
        image = io.BytesIO()
        await message.document.download(destination_file=image)
    # pylint: disable=bare-except
    except:
        mime = None
        image = None
    text = message.caption or ''
    cache = get(chat.id, {})

    await rm_last(chat, cache)
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    if mime and image and cache.get('s') == 'img':
        try:
            image = await upload(chat, image.read())
        except Exception as e:  # pylint: disable=broad-except
            await tg.send(
                chat.id,
                "Неверный формат, попробуй ещё раз",
                buttons=[{
                    'name': 'К посту', 'data': 'res',
                }],
            )
            await report.error(e, error=e)

        error, data = await api(chat, 'posts.save', {
            'id': cache.get('p'),
            'image': image,
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

    else:
        await report.important("Feedback", {
            'text': 'Document',
            **cache,
        })
        await tg.forward(cfg('bug_chat'), chat.id, message.message_id)

        text = "Передал твой запрос!"
        message_id = await tg.send(
            chat.id,
            text,
            buttons=[{'name': 'Мои посты', 'data': 'menu'}],
        )
        cache['m'] = message_id
        save(chat.id, cache)
