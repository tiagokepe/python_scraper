""" This module provides an abstract class used as interface to concrete classes"""
import json
import logging
from abc import ABC, abstractmethod
from logging import RootLogger, handlers
from typing import List

from pydantic import parse_obj_as

from models import Credential, UserProfile


class AbstractScraper(ABC):
    """
    AbstractScraper provides a common interface for scrapers such as:
    - log_in
    - load_user_profile
    It also provides common methods tha derived scrapers can inherit.
    """

    _credentials: List[Credential]
    _logger: RootLogger
    _user_profile: UserProfile

    @abstractmethod
    def __init__(self):
        self._logger = logging.getLogger("log/scraper.log")
        self._logger.setLevel(logging.DEBUG)
        log_handler = handlers.TimedRotatingFileHandler(
            "log/scraper.log", when="D", interval=1
        )
        log_handler.setLevel(logging.DEBUG)
        self._logger.addHandler(log_handler)

        # Load data
        with open("credentials.json", encoding="utf-8") as file:
            data = json.load(file)
            self._credentials = parse_obj_as(List[Credential], data["credentials"])

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def log_in(self) -> bool:
        """This method is called to log into the page

        Returns:
            bool: indicates successful to log into the page
        """

    @abstractmethod
    def load_user_profile(self) -> bool:
        """This method is called to lod user profile

        Returns:
            bool: indicates successful to load user profile
        """

    def save_user_profile(self):
        """This method saves loaded user profile to a json file"""
        # Write data to file
        with open("user_profile.json", "w", encoding="utf-8") as file:
            file.write(self._user_profile.json())
