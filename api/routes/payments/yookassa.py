"""
The YooKassa payment recieve method of the payment object of the API
"""

import time

from fastapi import APIRouter, Body
from pydantic import BaseModel

from models.user import User
from models.payment import Payment
from models.track import Track
from lib import cfg, report


DISCOUNT = cfg('discount')


router = APIRouter()


class Type(BaseModel):
    object: dict

# pylint: disable=too-many-branches
@router.post('/yookassa/')
async def pay(data: Type = Body(...)):
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
        Track(
            title='pay_ok',
            data={
                'value': value_real,
                'days': day,
            },
            user=user.id,
        ).save()

        # Update
        user.save()

        # TODO: TG notification

        # # Send sockets for real-time update
        # for socket in Socket.get(user=user_id, fields={}):
        #     await sio.emit('money_recieve', {
        #         'add': count,
        #         'balance': user.balance,
        #         'subscription': user.subscription,
        #     }, room=socket.id)

    except Exception as e:  # pylint: disable=broad-except
        await report.critical(str(e), error=e)

    return '', 200
