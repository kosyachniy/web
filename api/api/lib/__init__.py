"""
The main functionality for the API
"""

from consys.types import BaseType, validate
from libdev.cfg import cfg
from libdev.codes import get_network, get_language
from libdev.gen import generate, generate_id, generate_password

from api.lib.reports import report


__all__ = (
    'cfg',
    'get_network', 'get_language',
    'generate', 'generate_id', 'generate_password',
    'BaseType', 'validate',
    'report',
)
