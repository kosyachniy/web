"""
Functionality for working with Telegram
"""

# Libraries
## System
import json
import re

## External
import telebot


# Params
## Token
# pylint: disable=redefined-outer-name
with open('keys.json', 'r') as file:
    TG_TOKEN = json.loads(file.read())['tg']['token']


# Global variables
bot = telebot.TeleBot(TG_TOKEN)


# Funcs
def keyboard(rows, inline=False):
    """ Make keyboard """

    if rows == []:
        if inline:
            return telebot.types.InlineKeyboardMarkup()

        return telebot.types.ReplyKeyboardRemove()

    if rows in (None, [], [[]]):
        return rows

    if inline:
        buttons = telebot.types.InlineKeyboardMarkup()
    else:
        buttons = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    if not isinstance(rows[0], (list, tuple)):
        rows = [[button] for button in rows]

    for cols in rows:
        if inline:
            buttons.add(
                *[
                    telebot.types.InlineKeyboardButton(
                        col['name'],
                        **(
                            {'url': col['data']}
                            if col['type'] == 'link'
                            else {'callback_data': col['data']}
                        ),
                    ) for col in cols
                ]
            )
            # buttons.add(*[telebot.types.InlineKeyboardButton(col['name'], \
            # callback_data=col['data']) for col in cols])
        else:
            buttons.add(*[telebot.types.KeyboardButton(col) for col in cols])

    return buttons


def send(
    user, text='', buttons=None, inline=False, image=None, markup='Markdown',
):
    """ Send message """

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

def send_file(to, name):
    """ Send file """

    with open(name, 'rb') as file:
        return bot.send_document(to, file)

def delete(to, message, attempt=1):
    """ Delete message """

    try:
        bot.delete_message(to, message)

    except:
        if attempt == 1:
            delete(to, message, 2)

        raise Exception('Telegram del message')

def edit(to, message, text, buttons=None, inline=False, markup='Markdown'):
    """ Edit message """

    if '<img' in text:
        # img = re.search('<img src=".+">', text)[0].split('"')[1]
        # img = img.replace('/load', '../../data/load')[1:]
        text = re.sub('<img src=".+">', '', text)
        text = re.sub('\n\n\n\n', '\n\n', text)

        bot.edit_message_caption(
            chat_id=to,
            message_id=message,
            caption=text,
            reply_markup=keyboard(buttons, inline),
            parse_mode=markup,
        )

    else:
        bot.edit_message_text(
            chat_id=to,
            message_id=message,
            text=text,
            reply_markup=keyboard(buttons, inline),
            parse_mode=markup,
            disable_web_page_preview=True,
        )
