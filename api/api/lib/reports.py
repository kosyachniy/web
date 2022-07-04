"""
Reports functionality for the API
"""

from tgreports import Report

from api.lib import cfg


report = Report(cfg('mode'), cfg('tg.token'), cfg('bug_chat'))
