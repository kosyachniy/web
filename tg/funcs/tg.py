"""
Functionality for working with Telegram
"""

import io
import json
from copy import deepcopy

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import BotBlocked, CantParseEntities


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['tg']
    TG_TOKEN = sets['token']


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


def prepare_files(files):
    if isinstance(files, (list, tuple, set)):
        return [prepare_files(file) for file in files]

    if not isinstance(files, dict):
        files = {'data': files, 'type': 'image'}

    if files['type'] in {'location',}:
        return files

    if (
        isinstance(files['data'], io.BufferedReader)
        or (isinstance(files['data'], str) and files['data'][:4] != 'http')
    ):
        files['data'] = types.InputFile(files['data'])

    return files

def make_attachment(file, text=None, markup='MarkdownV2'):
    if isinstance(file['data'], str) and file['data'][:4] == 'http':
        return file['data']

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
    chat, text='', buttons=None, inline=False, files=None,
    markup='MarkdownV2', preview=False, reply=None, silent=False,
):
    """ Send message """

    # NOTE: Markup: https://core.telegram.org/bots/api#formatting-options
    # NOTE: ` reply ` doesn't work with multiple images / videos
    # TODO: next_message
    # TODO: more than 10 image / video

    if isinstance(chat, (list, tuple, set)):
        return [
            await send(
                el, text, buttons, inline, files,
                markup, preview, reply, silent,
            )
            for el in chat
        ]

    files_reserved = deepcopy(files)

    try:
        if files:
            files = prepare_files(files)

            if len(files) > 10:
                messages = []

                for i in range((len(files)-1)//10+1):
                    messages.extend(
                        await send(
                            chat, text, buttons, inline, files[i*10:(i+1)*10],
                            markup, preview, reply, silent,
                        )
                    )

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
                video = types.Video(files['data'])
                message = await bot.send_video(
                    chat,
                    video.file_id, # files['data'],
                    duration=video.duration,
                    width=video.width,
                    height=video.height,
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
            chat, text, buttons, inline, files_reserved,
            None, preview, reply, silent,
        )
    else:
        if isinstance(message, (list, tuple)):
            return [el['message_id'] for el in message]
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
