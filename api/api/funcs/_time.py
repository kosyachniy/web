"""
Time functionality for the API
"""

import time


def get_date(text, template='%Y%m%d'):
    """ Get date from timestamp """

    return time.strftime(template, time.localtime(text))
