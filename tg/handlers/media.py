import base64

from lib import api, cfg, report
from lib.tg import tg
from lib.queue import save, get
from middlewares.prepare_message import rm_last
from middlewares.check_user import check_user
from handlers.posts import send_post


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

    await rm_last(chat, cache)
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    if cache.get('s') == 'img':
        photo = 'data:image/jpg;base64,' + base64.b64encode(photo.read()).decode('utf-8')
        error, data = await api(chat, 'posts.save', {
            'id': cache.get('p'),
            'img': photo,
        })
        if error:
            message_id = await tg.send(chat.id, "Неверный формат, попробуй ещё раз", buttons=[{
                'name': 'К посту', 'data': 'res',
            }])
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

        text = "Передал твой фидбек!"
        message_id = await tg.send(
            chat.id,
            text,
            buttons=[{'name': 'Мои посты', 'data': 'menu'}],
        )
        cache['m'] = message_id
        save(chat.id, cache)

@tg.dp.message_handler(content_types=['any'])
async def handle_doc(message):
    """ Document handler """

    chat = message.chat
    try:
        mime = message.document.mime_type
        photo = await tg.bot.download_file(
            (await tg.bot.get_file(
                message.document.file_id
            )).file_path
        )
    except:
        mime = None
        photo = None
    text = message.caption or ''
    cache = get(chat.id, {})

    await rm_last(chat, cache)
    await tg.bot.send_chat_action(chat.id, action='typing')

    if await check_user(chat, True):
        return

    if mime and photo and cache.get('s') == 'img':
        try:
            photo = f"data:{mime};base64,{base64.b64encode(photo.read()).decode('utf-8')}"
        except Exception as e:
            await tg.send(chat.id, "Неверный формат, попробуй ещё раз", buttons=[{
                'name': 'К посту', 'data': 'res',
            }])
            await report.error(e, error=e)

        error, data = await api(chat, 'posts.save', {
            'id': cache.get('p'),
            'img': photo,
        })
        if error:
            message_id = await tg.send(chat.id, "Неверный формат, попробуй ещё раз", buttons=[{
                'name': 'К посту', 'data': 'res',
            }])
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

        text = "Передал твой фидбек!"
        message_id = await tg.send(
            chat.id,
            text,
            buttons=[{'name': 'Мои посты', 'data': 'menu'}],
        )
        cache['m'] = message_id
        save(chat.id, cache)
