"""
Sending SMS messages
"""

from . import cfg


LOGIN = cfg('smsc.login')
PASSWORD = cfg('password')


# TODO: Use pip/smsc
