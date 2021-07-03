"""
The main functionality for the API
"""

from ._types import check_params
from ._files import get_file, max_image, load_image, reimg
from ._time import get_date
from ._codes import get_network, get_language
from ._generate import generate, generate_password
from ._online import get_user, online_back, online_start, online_stop
from ._reports import report
