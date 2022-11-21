"""
Payments functionality for the API
"""

from libdev.cfg import cfg
# pylint: disable=import-error
from yookassa import Configuration # , Payment


Configuration.account_id = cfg('yookassa.id')
Configuration.secret_key = cfg('yookassa.secret')


def create(amount, description, data=None, renewal=None):
    """ Create a payment """

    req = {
        'amount': {
            'value': f'{amount}.00',
            'currency': 'RUB'
        },
        'description': description,
        'metadata': data,
    }

    if renewal:
        req['payment_method_id'] = renewal
    else:
        req['confirmation'] = {
            'type': 'embedded',
        }
        req['capture'] = True
        req['save_payment_method'] = True

    # return Payment.create(req).id
