""" This module provides the scraper states as an enum class.
    The scraper states are very usefull for testing proposal.
"""
from enum import Enum


class StateEnum(Enum):
    """Scraper state enum

    Args:
        Enum (): Defined five states for now.
    """

    STATELESS = 0
    INITIALIZED = 1
    LOGINTO = 2
    LOADED_PROFILE = 3
    LOGOUT = 4
