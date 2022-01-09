"""
The online socket of the account object of the API
"""

from consys.errors import ErrorWrong

from api.lib import BaseType, validate, report
from api.models.user import User
from api.models.token import Token
from api.models.job import Job
from api.models.socket import Socket
# from api.models.space import Space


# async def _get_active_space(user_id):
#     db_condition = {
#         # TODO: participant
#         # TODO: active
#     }

#     spaces = Space.get(**db_condition, fields={})

#     if spaces:
#         if len(spaces) > 1:
#             await report.warning("More than 1 active space", {
#                 'user': user_id,
#                 'spaces': [space.id for space in spaces],
#             })

#         return spaces[0].id

def _other_sessions(user_id, token=None):
    """ Checking for open online sessions of the user """

    if not user_id:
        if not token:
            return False

        sockets = Socket.get(token=token)

    else:
        sockets = Socket.get(user=user_id)

    return bool(sockets)

def _online_count():
    """ Counting the total number of online users """

    sockets = Socket.get(fields={'user', 'token'})
    count = len({socket.user or socket.token for socket in sockets})

    return count

def get_user(token_id, socket_id=None):
    """ Get user object by token """

    if token_id is not None:
        try:
            token = Token.get(token_id, fields={'user'})
        except ErrorWrong:
            token = Token(id=token_id)
            token.save()
        else:
            if token.user:
                return User.get(ids=token.user)

    elif socket_id is not None:
        try:
            socket = Socket.get(socket_id, fields={'user'})
        except ErrorWrong:
            pass
        else:
            if socket.user:
                return User.get(ids=socket.user)

    return User()

async def online_start(sio, token_id, socket_id=None):
    """ Start / update online session of the user """

    # TODO: save user data cache in db.sockets

    user = get_user(token_id)

    # Send socket about all online users to the user
    # TODO: Full info for all / auth / only for admins

    if socket_id:
        sockets_auth = Socket.get(user={'$exists': True}, fields={'user'})
        fields = {'id', 'login', 'avatar', 'name', 'surname', 'status'}
        users_uniq = [
            User.get(ids=socket.user, fields=fields).json(fields=fields)
            for socket in sockets_auth
            if socket.user not in {0, None}
        ]
        count = _online_count()

        if count:
            Job(
                method='online_add',
                users=[socket_id],
                data={
                    'count': count,
                    'users': users_uniq,
                },
            ).save()
            # await sio.emit('online_add', {
            #     'count': count,
            #     'users': users_uniq,
            # }, room=socket_id)

    # Already online
    already = _other_sessions(user.id, token_id)

    # Save current socket with user & token data
    if socket_id:
        changed = False

        try:
            socket = Socket.get(ids=socket_id, fields={'user'})
        except ErrorWrong:
            socket = Socket(
                id=socket_id,
                user=user.id,
                token=token_id,
            )
            changed = True

        else:
            if socket.token != token_id:
                socket.token = token_id
                changed = True
                await report.warning(
                    "Wrong socket.token",
                    {'from': socket.token, 'to': token_id},
                )

            if socket.user != user.id:
                socket.user = user.id
                changed = True
                await report.warning(
                    "Wrong socket.user",
                    {'from': socket.user, 'to': user.id},
                )

        if changed:
            socket.save()

    # Update other sockets by token

    sockets = Socket.get(token=token_id, fields={'user'})

    for socket in sockets:
        socket.user = user.id
        socket.save()

    # Send sockets

    if already:
        return

    # TODO: Сокет на обновление сессий в браузере

    # Send sockets about the user to all online users
    # TODO: Full info for all / auth / only for admins
    # NOTE: user.json(default=True) -> login, status

    count = _online_count()

    if user.id:
        data = [user.json(
            fields={'id', 'login', 'avatar', 'name', 'surname', 'status'}
        )]
    else:
        data = []

    Job(
        method='online_add',
        data={
            'count': count,
            'users': data,
        },
    ).save()
    # await sio.emit('online_add', {
    #     'count': count,
    #     'users': data,
    # })

    # # Redirect to active space
    # # TODO: cache
    # space = await _get_active_space(user.id)
    # if space:
    #     Job(
    #         method='space_return',
    #         users=[user.id],
    #         data={
    #             'id': space,
    #         },
    #     ).save()
    #     # for socket in Socket.get(user=user.id, fields={}):
    #     #     await sio.emit('space_return', {
    #     #         'id': space,
    #     #     }, room=socket.id)


class Type(BaseType):
    token: str

@validate(Type)
async def handle(request, data):
    """ Update online status """

    # TODO: Проверка, что токен не скомпрометирован - по ip?
    # TODO: Определить вкладку (tab - sid)

    await report.debug('ON', request.socket)

    if not data.token:
        await report.warning("Invalid token")
        return

    # Send sockets
    await online_start(request.sio, data.token, request.socket)

    # TODO: UTM parameters
    # TODO: Promos

    # user_id = user_current['id'] if user_current else 0
    # utms = Mark.get(token=data.token, user=user_id)

    # if utms:
    #     for utm in utms:
    #         utm.title = utm_mark
    #         utm.save()

    # else:
    #     utm = Mark(
    #         token=data.token,
    #         user=user_id,
    #         title=utm_mark,
    #     )

    #     utm.save()
