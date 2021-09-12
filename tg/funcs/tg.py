"""
Functionality for working with Telegram
"""

import io
import json

import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import BotBlocked, CantParseEntities


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    TG_TOKEN = sets['token']


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


def keyboard(rows, inline=False):
    """ Make keyboard

    None                → No changes
    [] / [[]]           → Clear keyboard
    [x, y]              → Button column
    [[x, y], [z]]       → Button table
    [[{'data': 'x'}]]   → Inline buttons
    """

    # Empty queries
    if rows is None:
        return

    # Type formation
    if isinstance(rows, (tuple, set)):
        rows = list(rows)
    elif not isinstance(rows, list):
        rows = [rows]

    # Inner elements formation
    for i in range(len(rows)):
        if not isinstance(rows[i], (list, tuple)):
            rows[i] = [rows[i]]

    # Clear
    if rows in ([], [[]]):
        if inline:
            return types.InlineKeyboardMarkup()

        return types.ReplyKeyboardRemove()

    # Determine mode
    if isinstance(rows[0][0], dict):
        inline = True

    # Base
    if inline:
        buttons = types.InlineKeyboardMarkup()
    else:
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Filling
    for cols in rows:
        if not inline:
            buttons.add(*[types.KeyboardButton(col) for col in cols])
            continue

        buttons.add(
            *[
                types.InlineKeyboardButton(
                    col['name'],
                    **(
                        {'url': col['data']}
                        if col['data'][:4] == 'http'
                        else {'callback_data': col['data']}
                    ),
                ) for col in cols
            ]
        )

    return buttons


async def send(
    chat, text='', buttons=None, inline=False, image=None, video=None,
    markup='MarkdownV2', preview=False, reply=None, silent=False,
):
    """ Send message """

    # NOTE: Markup: https://core.telegram.org/bots/api#formatting-options
    # TODO: next_message

    if isinstance(chat, (list, tuple, set)):
        return [
            await send(el, text, buttons, inline, image, markup, preview)
            for el in chat
        ]

    if video:
        image = video

    try:
        if image:
            if isinstance(image, io.BufferedReader):
                image = image.read()
            elif isinstance(image, str) and len(image) >= 4:
                if image[:4] == 'http':
                    image = requests.get(image).content
                else:
                    with open(image, 'rb') as file:
                        image = file.read()

            if video:
                message = await bot.send_video(
                    chat,
                    image,
                    caption=text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )
            else:
                message = await bot.send_photo(
                    chat,
                    image,
                    caption=text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

        else:
            message = await bot.send_message(
                chat,
                text,
                reply_markup=keyboard(buttons, inline),
                parse_mode=markup,
                disable_web_page_preview=not preview,
                disable_notification=silent,
                reply_to_message_id=reply,
                allow_sending_without_reply=True,
            )
    except BotBlocked:
        return 0
    except CantParseEntities:
        return await send(
            chat, text, buttons, inline, image,
            None, preview, reply, silent,
        )
    else:
        return message['message_id']

async def send_file(chat, file):
    """ Send file """

    return await bot.send_document(chat, file)

async def edit(
    chat, message, text='', buttons=None, inline=False,
    image=None, markup='Markdown', preview=False,
):
    """ Edit message """

    # TODO: change image

    if image:
        return await bot.edit_message_caption(
            chat,
            message_id=message,
            caption=text,
            reply_markup=keyboard(buttons, inline),
            parse_mode=markup,
        )

    return await bot.edit_message_text(
        chat,
        message_id=message,
        text=text,
		reply_markup=keyboard(buttons, inline),
		parse_mode=markup,
		disable_web_page_preview=not preview,
    )

async def delete(chat, message):
    """ Delete message """

    return await bot.delete_message(chat, message)

async def check_entry(chat, user):
    """ Check entry """

    try:
        user_type = await bot.get_chat_member(chat, user)

        if user_type.status in ('creator', 'administrator', 'member'):
            return True

        return False

    except: # FIXME: exception
        return False

async def forward(chat, from_chat, message, silent=False):
    """ Forward message """

    try:
        return await bot.forward_message(
            chat,
            from_chat,
            message,
            disable_notification=silent,
        )['message_id']
    except BotBlocked:
        return 0
