"""
Prepare message middleware
"""

from lib import report
from lib.tg import tg
from lib.queue import get
from middlewares.check_user import check_user


async def rm_last(chat, cache):
    """ Remove last message """
    if cache.get('m'):
        await tg.rm(chat.id, cache['m'])

async def prepare_message(data, action='typing'):
    """ Prepare new message """

    if 'message' in data:
        message = data.message
        callback = data
    else:
        message = data
        callback = None

    chat = message.chat
    if callback:
        text = callback.data
    else:
        text = message.text
    cache = get(chat.id, {})

    try:
        await rm_last(chat, cache)
        if action:
            await tg.bot.send_chat_action(chat.id, action=action)
        if callback:
            await tg.bot.answer_callback_query(callback.id)
    # pylint: disable=broad-except
    except Exception as e:
        await report.error("prepare_message", error=e)

    if await check_user(chat, True, text):
        return None, None, None

    return chat, text, cache
