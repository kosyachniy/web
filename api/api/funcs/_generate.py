"""
Codes generation functionality for the API
"""

import string
import random
import math


SYMBOLS = string.digits + string.ascii_letters
SPEC_SYMBOLS = '!@#$%&*-+=,./?|]~'


def generate(length: int = 32) -> str:
    """ Token / code generation """

    return ''.join(random.choice(SYMBOLS) for _ in range(length))

def generate_password(length: int = 8) -> str:
    """ Password generation """

    spec_symbols = ''.join(
        random.choice(SPEC_SYMBOLS) for _ in range(length//3)
    )
    digits = ''.join(
        random.choice(string.digits) for _ in range(length//3)
    )
    letters = ''.join(
        random.choice(string.ascii_letters) for _ in range(math.ceil(length/3))
    )

    data = list(spec_symbols + digits + letters)
    random.shuffle(data)
    data = ''.join(data)

    return data
