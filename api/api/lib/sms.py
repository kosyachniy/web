"""
Sending SMS messages
"""

from api.lib import cfg


LOGIN = cfg('smsc.login')
PASSWORD = cfg('password')


# TODO: Use pip/smsc
