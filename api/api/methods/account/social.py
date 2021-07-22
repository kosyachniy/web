"""
The authorization via social networks method of the account object of the API
"""

# import urllib
# import base64

# import requests

from ...funcs import BaseType, validate # online_start
from ...errors import ErrorAccess # ErrorInvalid, ErrorWrong


class Type(BaseType):
    user: int
    # TODO: code: str

# pylint: disable=unused-argument
@validate(Type)
async def handle(this, request, data):
    """ By social network """

    # TODO: reports
    # TODO: actions

    # No access
    if request.user.status < 2:
        raise ErrorAccess('social')

    # user_id = 0
    # new = False
    # mail = ''

    # # ВКонтакте
    # if data.id == 1:
    #     link = 'https://oauth.vk.com/access_token?client_id={}&client_secret=' \
    #            '{}&redirect_uri={}callback&code={}'
    #     response = json.loads(
    #         requests.get(
    #             link.format(
    #                 this.vk['client_id'],
    #                 this.vk['client_secret'],
    #                 this.client,
    #                 data.code,
    #             )
    #         ).text
    #     )

    #     if 'user_id' in response:
    #         user_id = response['user_id']
    #     else:
    #         raise ErrorAccess('code')

    #     if 'email' in response:
    #         mail = response['email']

    # # Google
    # elif data.id == 3:
    #     link = 'https://accounts.google.com/o/oauth2/token'
    #     cont = {
    #         'client_id': this.google['client_id'],
    #         'client_secret': this.google['client_secret'],
    #         'redirect_uri': '{}callback'.format(this.client),
    #         'grant_type': 'authorization_code',
    #         'code': urllib.parse.unquote(data.code),
    #     }
    #     response = json.loads(requests.post(link, json=cont).text)

    #     if 'access_token' not in response:
    #         raise ErrorAccess('code')

    #     link = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'
    #     response = json.loads(
    #         requests.get(
    #             link.format(response['access_token'])
    #         ).text
    #     )

    #     if 'id' in response:
    #         user_id = response['id']
    #     else:
    #         raise ErrorAccess('code')

    # # Wrong ID

    # if not user_id:
    #     raise ErrorWrong('id')

    # # Sign in

    # db_condition = {
    #     'social': {'$elemMatch': {'id': data.id, 'user': user_id}},
    # }

    # db_filter = {
    #     '_id': False,
    #     'id': True,
    #     'login': True,
    #     'name': True,
    #     'surname': True,
    #     'avatar': True,
    #     'status': True,
    #     'mail': True,
    #     # 'rating': True,
    #     # 'balance': True,
    # }

    # res = db.users.find_one(db_condition, db_filter)

    # # Wrong password
    # if not res:
    #     # Check keys

    #     name = ''
    #     surname = ''
    #     login = ''
    #     avatar = None

    #     if data.id == 1:
    #         if 'access_token' in response:
    #             token = response['access_token']
    #         else:
    #             raise ErrorAccess('code')

    #         # link = 'https://api.vk.com/method/account.getProfileInfo' \
    #         #        '?access_token={}&v=5.103'
    #         link = 'https://api.vk.com/method/users.get?user_ids={}&fields=' \
    #                'photo_max_orig,nickname&access_token={}&v=5.103'

    #         try:
    #             response = json.loads(
    #                 requests.get(
    #                     link.format(user_id, token)
    #                 ).text
    #             )['response'][0]
    #         except:
    #             raise ErrorAccess('vk')

    #         try:
    #             name = response['first_name']
    #             _check_name(name)
    #         except Exception:
    #             name = ''

    #         try:
    #             surname = response['last_name']
    #             _check_surname(surname)
    #         except Exception:
    #             surname = ''

    #         try:
    #             login = response['nickname']
    #             _check_login(login, request.user)
    #         except Exception:
    #             login = ''

    #         try:
    #             avatar = str(base64.b64encode(
    #                 requests.get(response['photo_max_orig']).content
    #             ))[2:-1]
    #         except Exception:
    #             avatar = None

    #         try:
    #             if mail:
    #                 _check_mail(mail, request.user)
    #         except Exception:
    #             mail = ''

    #     elif data.id == 3:
    #         # link = 'https://www.googleapis.com/oauth2/v1/userinfo' \
    #         #        '?access_token={}'.format(data.data['access_token'])
    #         # res_google = json.loads(requests.get(link).text)

    #         try:
    #             name = response['given_name']
    #             _check_name(name)
    #         except Exception:
    #             name = ''

    #         try:
    #             surname = response['family_name']
    #             _check_surname(surname)
    #         except Exception:
    #             surname = ''

    #         try:
    #             mail = response['email']
    #             _check_mail(mail, request.user)
    #         except Exception:
    #             mail = ''

    #         try:
    #             if response['picture']:
    #                 avatar = str(base64.b64encode(
    #                     requests.get(response['picture']).content
    #                 ))[2:-1]
    #         except Exception:
    #             pass

    #     # Sign up

    #     db_condition = {
    #         'social': {'$elemMatch': {'user': user_id}},
    #     }

    #     db_filter = {
    #         '_id': True,
    #     }

    #     user = db.users.find_one(db_condition, db_filter)

    #     if user:
    #         raise ErrorWrong('hash')

    #     # Sign up
    #     else:
    #         new = True

    #         user = _registrate(
    #             request.user,
    #             request.timestamp,
    #             social=[{
    #                 'id': data.id,
    #                 'user': user_id,
    #             }],
    #             name=name,
    #             surname=surname,
    #             avatar=avatar,
    #             mail=mail,
    #         )

    #         #

    #         db_filter = {
    #             '_id': False,
    #             'id': True,
    #             'status': True,
    #             # 'balance': True,
    #             # 'rating': True,
    #             'login': True,
    #             'name': True,
    #             'surname': True,
    #             'mail': True,
    #         }

    #         user = db.users.find_one({'id': user['id']}, db_filter)

    # # Assignment of the token to the user

    # if not request.token:
    #     raise ErrorInvalid('token')

    # req = {
    #     'token': request.token,
    #     'user': user['id'],
    #     'time': request.timestamp,
    # }
    # db.tokens.insert_one(req)

    # # Update online users

    # await online_start(this.sio, request.token)

    # # Response

    # res = {
    #     'id': user['id'],
    #     'login': user['login'],
    #     'name': user['name'],
    #     'surname': user['surname'],
    #     'status': user['status'],
    #     'mail': user['mail'],
    #     # 'balance': user['balance'],
    #     # 'rating': user['rating'],
    #     'new': new,
    # }

    # if 'avatar' in user:
    #     res['avatar'] = '/load/opt/' + user['avatar']
    # else:
    #     res['avatar'] = 'user.png'

    # return res
