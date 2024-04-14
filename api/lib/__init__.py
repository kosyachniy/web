"""
The main functionality for the API
"""

from consys.types import BaseType, validate
from libdev.cfg import cfg
from libdev.gen import generate, generate_id, generate_password
from loguru import logger as log


__all__ = (
    "cfg",
    "log",
    "generate",
    "generate_id",
    "generate_password",
    "BaseType",
    "validate",
)
