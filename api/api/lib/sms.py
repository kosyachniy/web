"""
Sending SMS messages
"""

from libdev.cfg import cfg


USER = cfg('smsc.user')
PASS = cfg('smsc.pass')


# TODO: Use pip/smsc
