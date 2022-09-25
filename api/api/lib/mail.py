"""
Managing address books, sending mail
"""

from libdev.cfg import cfg
# pylint: disable=import-error
from pysendpulse.pysendpulse import PySendPulse


MEMCACHED_HOST = '127.0.0.1:11211'


mail = PySendPulse(
    user_id=cfg('sendpulse.id'),
    secret=cfg('sendpulse.secret'),
    storage_type='memcached',
    memcached_host=MEMCACHED_HOST,
)
