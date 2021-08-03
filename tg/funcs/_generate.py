"""
Codes generation functionality for the Telegram bot
"""

import string
import random


SYMBOLS = string.digits + string.ascii_letters


def generate(length: int = 32) -> str:
    """ Token / code generation """

    return ''.join(random.choice(SYMBOLS) for _ in range(length))
