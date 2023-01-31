"""
Analytics
"""

import asyncio

from libdev.time import get_time

from lib import cfg, report
# pylint: disable=import-error
from lib.docs import open_sheets
from models.user import User
from models.post import Post


STEPS = [
    "Not visited",
    "Not registered",
    "Not filled profile",
    "Not added post",
    "Not added second",
    "Everything done",
]


sheets = open_sheets(cfg('ANALYTICS_SHEET'))


def get_funnel(users_reg, users_fill, users_save, users_second, utm=None):
    """ Get formatted funnel """

    data = []

    reg_count = len({k for k, v in users_reg.items() if not utm or v == utm})
    fill_count = len({k for k, v in users_fill.items() if not utm or v == utm})
    save_count = len({k for k, v in users_save.items() if not utm or v == utm})
    second_count = len({
        k
        for k, v in users_second.items()
        if not utm or v == utm
    })

    data.append([
        utm or "Σ", "",
        reg_count, fill_count, save_count, second_count,
    ])
    data.append([
        "", "", "",
        f"{round(fill_count * 100 / reg_count, 1) if reg_count else '-'}%",
        f"{round(save_count * 100 / fill_count, 1) if fill_count else '-'}%",
        f"{round(second_count * 100 / save_count, 1) if save_count else '-'}%",
    ])
    data.append([
        "", "", "",
        f"{round(fill_count * 100 / reg_count, 1) if reg_count else '-'}%",
        f"{round(save_count * 100 / reg_count, 1) if reg_count else '-'}%",
        f"{round(second_count * 100 / reg_count, 1) if reg_count else '-'}%",
    ])

    return data

# pylint: disable=too-many-branches
async def analytics():
    """ Get funnel """

    utms = set()
    users = {}
    users_reg = {}
    users_fill = {}
    users_save = {}
    users_second = {}

    for user in User.get():
        utms.add(user.utm)
        users_reg[user.id] = user.utm

        social = user.get_social(2)
        if social is None:
            contact = ""
        elif social['login']:
            contact = f"https://t.me/{social['login']}"
        else:
            contact = f"tg://user?id={social['id']}"

        users[user.id] = {
            'id': user.id,
            'name': user.title,
            'contact': contact,
            'source': user.utm,
            'created': "MSK " + get_time(
                user.created + 10800,
                '%d.%m.%Y %H:%M'
            ),
            'posts': 0,
        }

        filled = (
            bool(user.name) + bool(user.surname)
            + bool(user.image) + bool(user.login)
        )
        if filled:
            users_fill[user.id] = users_reg[user.id]


    for post in Post.get():
        if not post.user:
            continue

        users[post.user]['posts'] += 1
        if post.user in users_save:
            users_second[post.user] = users_reg[post.user]
        else:
            users_save[post.user] = users_reg[post.user]

    data = [[
        "UTM", "",
        "Registered", "Filled profile", "Added post", "Added second",
    ]]
    data += get_funnel(users_reg, users_fill, users_save, users_second)

    for utm in utms:
        if not utm:
            continue

        data += [[]] + get_funnel(
            users_reg, users_fill, users_save, users_second,
            utm=utm,
        )

    sheets[0].clear()
    sheets[0].update(data)

    # TODO: merging cells
    data = [[
        "ID", "Name", "Contact",
        "Source", "Registered",
        "Posts count", "Step", "Target action",
    ]]

    for user in users.values():
        step = 1
        if step == 1 and user['id'] in users_reg:
            step = 2
        if step == 2 and user['id'] in users_fill:
            step = 3
        if step == 3 and user['id'] in users_save:
            step = 4
        if step == 4 and user['id'] in users_second:
            step = 5

        data.append([
            user['id'],
            user['name'],
            user['contact'],
            user['source'],
            user['created'],
            user['posts'],
            step,
            STEPS[step],
        ])

    sheets[1].clear()
    sheets[1].update(data)


async def handle(_):
    """ Analytics """

    if cfg('mode') not in {'PRE', 'PROD'}:
        return

    while True:
        try:
            count = await analytics()
        except Exception as e:  # pylint: disable=broad-except
            count = None
            await report.critical(str(e), error=e)

        if count is None:
            await asyncio.sleep(10800)  # 3 hours
