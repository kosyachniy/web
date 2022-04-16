"""
Sending SMS messages
"""

from api.lib import cfg


USER = cfg('smsc.user')
PASS = cfg('smsc.pass')


# TODO: Use pip/smsc
