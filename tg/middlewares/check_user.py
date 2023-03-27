"""
User checking middleware
"""

from lib import auth, report, user_ids, user_logins, user_statuses, user_titles
from lib.tg import tg
from lib.queue import get, save


async def check_user(chat, public=False, text=None, locale=None, image=None):
    """ Authorize user and check access """

    utm = None
    if text and ' ' in text:
        utm = text.split()[1]
    if utm == 'auth':
        utm = None

    res = await auth(chat, utm, locale, image)

    if res is None:
        cache = get(chat.id, {})
        message_id = await tg.send(
            chat.id,
            "Бот умер 😵‍💫\nМеня уже лечат!",
            buttons=[{'name': 'Мои посты', 'data': 'menu'}],
        )
        cache['m'] = message_id
        save(chat.id, cache)
        await report.error("Check user", {'user': chat.id})
        return True

    if not public and user_statuses[chat.id] < 4:
        await tg.send(
            chat.id,
            "Нет доступа 😛",
            buttons=[{'name': 'Мои посты', 'data': 'menu'}],
        )
        await report.important("Illegal access", {
            'user': user_ids[chat.id],
            'name': user_titles[chat.id],
            'social_user': chat.id,
            'social_login': user_logins[chat.id],
            'status': user_statuses[chat.id],
            'utm': text,
        })
        return True
