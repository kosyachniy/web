"""
Functionality for working with Telegram
"""

import io
import json
from copy import deepcopy
from typing import Union, Optional

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import (
    BotBlocked, CantParseEntities, MessageToDeleteNotFound, ChatNotFound,
)


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    TG_TOKEN = sets['token']

TEXT_LIMIT = 4096
CAPTION_LIMIT = 1024
FILES_LIMIT = 10


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


def prepare_files(files):
    """ Prepare a file for single sending """

    if isinstance(files, (list, tuple, set)):
        data, reserv = zip(*[prepare_files(file) for file in files])
        return list(data), list(reserv)

    if not isinstance(files, dict):
        files = {'data': files, 'type': 'image'}

    if files['type'] in {'location',}:
        return files, files

    if isinstance(files['data'], dict):
        reserv = deepcopy(files)
        files['data'] = types.InputFile(
            io.BytesIO(files['data']['data']),
            files['data']['name'],
        )
        return files, reserv

    if not (
        isinstance(files['data'], io.BufferedReader)
        or (isinstance(files['data'], str) and files['data'][:4] != 'http')
    ):
        return files, files

    file = types.InputFile(files['data'])

    if files['type'] in {'video',}:
        files['data'] = file.file.read()
        return files, files

    file = {'name': file.filename, 'data': file.file.read()}
    files['data'] = types.InputFile(io.BytesIO(file['data']), file['name'])

    return files, {'data': file, 'type': files['type']}

def make_attachment(file, text=None, markup='MarkdownV2'):
    """ Prepare a file for multiple sending """

    if isinstance(file['data'], str) and file['data'][:4] == 'http':
        return file['data']

    if isinstance(file['data'], bytes):
        file['data'] = io.BytesIO(file['data'])

    if file['type'] == 'image':
        return types.InputMediaPhoto(
            file['data'],
            caption=text,
            parse_mode=markup,
        )

    if file['type'] == 'video':
        return types.InputMediaVideo(
            file['data'],
            caption=text,
            parse_mode=markup,
        )

    if file['type'] == 'audio':
        return types.InputMediaAudio(
            file['data'],
            caption=text,
            title=file.get('title'),
            performer=file.get('performer'),
            parse_mode=markup,
        )

    return types.InputMediaDocument(
        file['data'],
        caption=text,
        parse_mode=markup,
    )

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
    for i, el in enumerate(rows):
        if not isinstance(el, (list, tuple)):
            rows[i] = [el]

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


# pylint: disable=too-many-arguments
async def send(
    chat: Union[int, str, list, tuple, set],
    text: Optional[str] = '',
    buttons: Optional[Union[list, tuple, set, str]] = None,
    inline: Optional[bool] = False,
    files: Optional[Union[
        str, list, tuple, set, bytes, io.BufferedReader,
    ]] = None,
    markup: Optional[str] = 'MarkdownV2',
    preview: Optional[bool] = False,
    reply: Optional[Union[int, str]] = None,
    silent: Optional[bool] = False,
):
    """ Send message """

    # NOTE: Markup: https://core.telegram.org/bots/api#formatting-options
    # NOTE: ` reply ` doesn't work with multiple images / videos
    # TODO: next_message

    if isinstance(chat, (list, tuple, set)):
        return [
            await send(
                el, text, buttons, inline, files,
                markup, preview, reply, silent,
            )
            for el in chat
        ]

    try:
        if files:
            files, reserv = prepare_files(files)

            if len(files) > FILES_LIMIT:
                messages = []

                for i in range((len(files)-1)//FILES_LIMIT+1):
                    message = await send(
                        chat, text, buttons, inline,
                        files[i*FILES_LIMIT:(i+1)*FILES_LIMIT],
                        markup, preview, reply, silent,
                    )

                    if message is None:
                        return None

                    messages.extend(message)

                return messages

            if text and len(text) > CAPTION_LIMIT:
                messages = []

                message = await send(
                    chat, text[:CAPTION_LIMIT],
                    buttons, inline, reserv, markup, preview, reply, silent,
                )

                if message is None:
                    return None

                messages.extend(message)

                for i in range(1, (len(text)-1)//CAPTION_LIMIT+1):
                    message = await send(
                        chat, text[i*CAPTION_LIMIT:(i+1)*CAPTION_LIMIT],
                        buttons, inline, None, markup, preview, reply, silent,
                    )

                    if message is None:
                        return None

                    messages.extend(message)

                return messages

            if isinstance(files, list):
                media = types.MediaGroup()
                media.attach_photo(make_attachment(files[0], text, markup))

                for el in files[1:]:
                    media.attach_photo(make_attachment(el))

                message = await bot.send_media_group(
                    chat,
                    media,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

            elif files['type'] == 'image':
                message = await bot.send_photo(
                    chat,
                    files['data'],
                    caption=text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

            elif files['type'] == 'video':
                message = await bot.send_video(
                    chat,
                    files['data'],
                    caption=text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

            elif files['type'] == 'audio':
                message = await bot.send_audio(
                    chat,
                    files['data'],
                    caption=text,
                    title=files.get('title'),
                    performer=files.get('performer'),
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

            elif files['type'] == 'animation':
                message = await bot.send_animation(
                    chat,
                    files['data'],
                    caption=text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

            elif files['type'] == 'voice':
                message = await bot.send_voice(
                    chat,
                    files['data'],
                    caption=text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

            elif files['type'] == 'video_note':
                message = await bot.send_video_note(
                    chat,
                    files['data'],
                    duration=files.get('duration'),
                    length=files.get('length'),
                    reply_markup=keyboard(buttons, inline),
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

            elif files['type'] == 'location':
                message = await bot.send_location(
                    chat,
                    files['data']['lat'],
                    files['data']['lng'],
                    reply_markup=keyboard(buttons, inline),
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

            else:
                message = await bot.send_document(
                    chat,
                    files['data'],
                    caption=text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

        else:
            reserv = None

            if text and len(text) > TEXT_LIMIT:
                messages = []

                for i in range((len(text)-1)//TEXT_LIMIT+1):
                    message = await send(
                        chat, text[i*TEXT_LIMIT:(i+1)*TEXT_LIMIT], buttons,
                        inline, reserv, markup, preview, reply, silent,
                    )

                    if message is None:
                        return None

                    messages.extend(message)

                return messages

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
        return None
    except CantParseEntities:
        return await send(
            chat, text, buttons, inline, reserv,
            None, preview, reply, silent,
        )

    if isinstance(message, (list, tuple)):
        return [el['message_id'] for el in message]

    return [message['message_id']]

async def edit(
    chat: Union[int, str],
    message: Union[int, str],
    text: Optional[str] = '',
    buttons: Optional[Union[list, tuple, set, str]] = None,
    inline: Optional[bool] = False,
    files: Optional[Union[
        str, list, tuple, set, bytes, io.BufferedReader,
    ]] = None,
    markup: Optional[str] = 'MarkdownV2',
    preview: Optional[bool] = False,
):
    """ Edit message """

    # NOTE: 1 file per 1 message

    if files is not None:
        res = None

        if files:
            files, _ = prepare_files(files)

            if isinstance(files, (list, tuple, set)):
                media = types.MediaGroup()

                for el in files:
                    media.attach_photo(make_attachment(el))

            else:
                media = make_attachment(files)

            res = await bot.edit_message_media(
                media,
                chat,
                message,
                reply_markup=keyboard(buttons, inline),
            )

        if text is not None:
            res = await bot.edit_message_caption(
                chat,
                message,
                caption=text,
                reply_markup=keyboard(buttons, inline),
                parse_mode=markup,
            )

        return res['message_id'] if res is not None else None

    return (await bot.edit_message_text(
        text,
        chat,
        message,
		reply_markup=keyboard(buttons, inline),
		parse_mode=markup,
		disable_web_page_preview=not preview,
    ))['message_id']

async def delete(
    chat: Union[int, str],
    message: Union[int, str, list, tuple, set],
):
    """ Delete message """

    if isinstance(message, (list, tuple, set)):
        return [
            await delete(chat, el)
            for el in message
        ]

    try:
        return await bot.delete_message(chat, message)
    except MessageToDeleteNotFound:
        return False

async def check_entry(
    chat: Union[int, str],
    user: Union[int, str],
):
    """ Check a user entry into a chat """

    try:
        user_type = await bot.get_chat_member(chat, user)
        return user_type.status in ('creator', 'administrator', 'member')
    except ChatNotFound:
        return False

async def forward(
    chat: Union[int, str],
    from_chat: Union[int, str],
    message: Union[int, str],
    silent: Optional[bool] = False,
):
    """ Forward message """

    try:
        return (await bot.forward_message(
            chat,
            from_chat,
            message,
            disable_notification=silent,
        ))['message_id']
    except BotBlocked:
        return 0
