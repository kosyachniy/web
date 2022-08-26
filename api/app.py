"""
API Endpoints (Transport level)
"""

# pylint: disable=wrong-import-order,wrong-import-position,ungrouped-imports

# Main app
from fastapi import FastAPI, Request
app = FastAPI(title='Web app API')

# # Prometheus
# from prometheus_fastapi_instrumentator import Instrumentator
# Instrumentator().instrument(app).expose(app)

# CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Socket.IO
import socketio
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
asgi = socketio.ASGIApp(sio)

# # Limiter

# from flask import request, jsonify
# from flask_limiter import Limiter

# def get_ip():
#     try:
#         if 'ip' in request.json:
#             return request.json['ip']

#     except:
#         pass

#     return request.remote_addr

# limiter = Limiter(
#     app,
#     key_func=get_ip,
#     default_limits=['1000/day', '500/hour', '20/minute']
# )

# API
import time
# import json
# from functools import wraps

# import jwt
from pydantic import BaseModel
from consys.errors import BaseError

from api import API
from api.lib import cfg, report
from api.models.user import User
from api.models.action import Action
from api.models.socket import Socket
from api.models.payment import Payment


api = API(
    sio=sio,
)

# ## JWT
# def token_required(f):
#     @wraps(f)
#     async def decorated(data, request):
#         try:
#             header = request.headers.get('Authorization')

#             if not header:
#                 return await f(data, request)

#             token = header.split(' ')[1]

#             if not token or token == 'null':
#                 return await f(data, request)

#             try:
#                 data.jwt = jwt.decode(token, cfg('jwt'), algorithms='HS256')
#             except Exception as e:
#                 await report.error("Invalid token", {
#                     'token': token,
#                     'error': e,
#                 })
#                 return json.dumps({'message': 'Token is invalid!'}), 403

#             return await f(data, request)

#         except Exception as e:
#             await report.error("JWT handler", {
#                 'data': data,
#                 'error': e,
#             })
#             return await f(data, request)

#     return decorated

## Endpoints
### Main
class Input(BaseModel):
    """ Main endpoint model """
    method: str
    params: dict = {}
    network: str = ''
    locale: str = None
    token: str = None
    socket: str = None
    jwt: dict = None

@app.post('/')
# @token_required
async def index(data: Input, request: Request):
    """ Main API endpoint """

    # print(data, request.client.host, request.client.port)

    # Call API

    req = {}

    try:
        res = await api.method(
            data.method,
            data.params,
            ip=request.client.host,
            token=data.token,
            socket=data.socket,
            network=data.network,
            locale=data.locale,
            jwt=data.jwt,
        )

    except BaseError as e:
        req['error'] = e.code
        req['data'] = str(e.txt) # TODO: Fix in consys.errors

    # pylint: disable=broad-except
    except Exception as e:
        req['error'] = 1
        req['data'] = "Server error"
        await report.critical(str(e), error=e)

    else:
        req['error'] = 0

        if res is not None:
            req['data'] = res

    # Response
    return req

### Payments
DISCOUNT = cfg('discount')

class InputPayment(BaseModel):
    """ Payment endpoint model """

    object: dict

# pylint: disable=too-many-branches
@app.post('/pay/ya/')
async def pay(data: InputPayment, request: Request):
    """ Payments endpoint """

    data = data.object

    count = float(data.get('amount', {}).get('value') or 0)
    user_id = data.get('metadata', {}).get('user')

    if not user_id:
        await report.warning("Wrong user", {
            'metadata': data.get('metadata'),
        })
        return '', 200

    user_id = int(user_id)
    user = User.get(user_id)
    timestamp = int(time.time())

    # Initial balance
    value_real = count + 0

    try:
        # if user.preprice:
        #     discount_real = None
        #     day = 1
        #     user.limit = 1
        #     del user.preprice

        # elif user.price:
        #     discount_real = None
        #     day = 30 if count == user.price else 90
        #     del user.limit
        #     del user.price

        discount_real = user.discount + 0 if user.discount else DISCOUNT
        if discount_real:
            count /= discount_real

            if user.discount: # TODO: Fix in consys.model
                del user.discount

        # Crediting funds
        if count >= cfg('subscription.year'):
            day = 365
        elif count >= cfg('subscription.ay'):
            day = 270
        elif count >= cfg('subscription.season'):
            day = 90
        elif count >= cfg('subscription.month'):
            day = 30
        elif count >= cfg('subscription.week'):
            day = 7
        elif count >= cfg('subscription.day'):
            day = 1
        else:
            day = 0
            await report.warning("Too little to pay for a subscription", {
                'value': count,
                'user': user_id,
            })

        # del user.limit

        # Save payment data

        payment = Payment(
            id=data['payment_method']['id'],
            type=data['payment_method']['type'],
            card={
                'type': data['payment_method']['card'].get('card_type'),
                'bank': data['payment_method']['card'].get('issuer_name'),
                'country': data['payment_method']['card'].get('issuer_country'),
                'first': data['payment_method']['card'].get('first6'),
                'last': data['payment_method']['card'].get('last4'),
                'expired': {
                    'month': data['payment_method']['card'].get('expiry_month'),
                    'year': data['payment_method']['card'].get('expiry_year'),
                },
            } if data['payment_method'].get('card') else None,
            value=int(count),
            currency=data['amount']['currency'],
            discount=discount_real,
        )

        if data['payment_method']['saved']:
            user.pay = [payment.json(default=False)] # TODO: Fix in consys.model

        # Report
        await report.important("Payment", {
            'service': 'yandex',
            'type': payment.type,
            'card': payment.card,
            'value': f"{int(value_real)} {payment.currency}",
            'user': f"#{user_id} {user.name} {user.surname}",
            'discount': user.discount and f"{int((1-user.discount)*100)}%",
            'renewal': data['payment_method']['saved'],
        }, tags=['payment'])

        if day:
            user.subscription = max(user.subscription, timestamp) + 86400 * day

        # Action tracking
        action = Action(
            title='pay_ok',
            data={
                'value': value_real,
                'days': day,
            },
        )
        user.actions.append(action.json(default=False))

        # Update
        user.save()

        # TODO: TG notification

        # Send sockets for real-time update
        for socket in Socket.get(user=user_id, fields={}):
            await sio.emit('money_recieve', {
                'add': count,
                'balance': user.balance,
                'subscription': user.subscription,
            }, room=socket.id)

    # pylint: disable=broad-except
    except Exception as e:
        await report.critical(str(e), error=e)

    return '', 200

# ### Facebook bot
# @app.route('/fb', methods=['POST'])
# @app.route('/fb/', methods=['POST'])
# def fb():
#     x = request.json
#     print(x)
#     return jsonify({'qwe': 'asd'})


# Online users

@sio.on('connect')
async def connect(sid, request, data):
    """ Connect socket """
    await api.method(
        'account.connect',
        ip=request['asgi.scope']['client'][0],
        socket=sid,
    )

@sio.on('online')
async def online(sid, data):
    """ Socket about online user """
    await api.method(
        'account.online',
        data,
        socket=sid,
    )

@sio.on('disconnect')
async def disconnect(sid):
    """ Disconnect socket """
    await api.method(
        'account.disconnect',
        socket=sid,
    )


app.mount('/', asgi) # TODO: check it
