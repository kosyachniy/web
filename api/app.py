"""
API Endpoints (Transport level)
"""

# pylint: disable=wrong-import-order,wrong-import-position,ungrouped-imports

# Main app
from fastapi import FastAPI, Request
app = FastAPI(title='Web app API')

# Prometheus
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

# CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

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

from pydantic import BaseModel
from consys.errors import BaseError
from libdev.cfg import cfg

from api import API
from api.lib import report
from api.models.user import User
from api.models.action import Action
from api.models.job import Job
# from api.models.socket import Socket
from api.models.payment import Payment


api = API(
    # sio=sio,
)

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

@app.post('/')
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
    discount_real = user.discount + 0 if user.discount else DISCOUNT
    if discount_real:
        count /= discount_real

        if user.discount: # TODO: Fix in consys.model
            del user.discount

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
    Job(
        method='money_recieve',
        users=[user_id],
        data={
            'add': count,
            'balance': user.balance,
            'subscription': user.subscription,
        },
    ).save()
    # for socket in Socket.get(user=user_id, fields={}):
    #     await sio.emit('money_recieve', {
    #         'add': count,
    #         'balance': user.balance,
    #         'subscription': user.subscription,
    #     }, room=socket.id)

    return '', 200

# ### Facebook bot
# @app.route('/fb', methods=['POST'])
# @app.route('/fb/', methods=['POST'])
# def fb():
#     x = request.json
#     print(x)
#     return jsonify({'qwe': 'asd'})


# app.mount('/', asgi) # TODO: check it
