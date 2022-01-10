"""
Sending SMS messages
"""

from api.lib import cfg


LOGIN = cfg('smsc.login')
PASSWORD = cfg('smsc.password')


# TODO: Use pip/smsc
