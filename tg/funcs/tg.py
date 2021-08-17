"""
Functionality for working with Telegram
"""

import json

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    TG_TOKEN = sets['token']


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


def keyboard(rows, inline=False):
    """ Make keyboard """

    if rows == []:
        if inline:
            return types.InlineKeyboardMarkup()

        return types.ReplyKeyboardRemove()

    if rows in (None, [], [[]]):
        return rows

    if inline:
        buttons = types.InlineKeyboardMarkup()
    else:
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if not isinstance(rows[0], (list, tuple)):
        rows = [[button] for button in rows]

    for cols in rows:
        if inline:
            buttons.add(
                *[
                    types.InlineKeyboardButton(
                        col['name'],
                        **(
                            {'url': col['data']}
                            if 'type' in col and col['type'] == 'link'
                            else {'callback_data': col['data']}
                        ),
                    ) for col in cols
                ]
            )
            # buttons.add(*[types.InlineKeyboardButton(col['name'], \
            # callback_data=col['data']) for col in cols])
        else:
            buttons.add(*[types.KeyboardButton(col) for col in cols])

    return buttons

def send(
    user, text='', buttons=None, inline=False, image=None, markup='Markdown',
):
    """ Send message """

    # TODO: users=[], forward=None, next_message=func
    # TODO: Если пустой buttons - убирать кнопки (но не None)
    # TODO: return bot.forward_message(user, forward, text)

    if not image:
        return bot.send_message(
            user,
            text,
            reply_markup=keyboard(buttons, inline),
            parse_mode=markup,
            disable_web_page_preview=True,
        )

    return bot.send_photo(
        user,
        image,
        text,
        reply_markup=keyboard(buttons, inline),
        parse_mode=markup,
    )
