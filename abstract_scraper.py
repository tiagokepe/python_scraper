import json
import logging
import logging.handlers as handlers
from logging import RootLogger
from abc import ABC, abstractmethod
from models import Credential
from models import UserProfile
from pydantic import parse_obj_as
from typing import List


class AbstractScraper(ABC):
    _credentials: List[Credential]
    _logger: RootLogger
    _user_profile: UserProfile

    @abstractmethod
    def __init__(self):
        self._logger = logging.getLogger("log/scraper.log")
        self._logger.setLevel(logging.DEBUG)
        logHandler = handlers.TimedRotatingFileHandler(
            "log/scraper.log", when="D", interval=1
        )
        logHandler.setLevel(logging.DEBUG)
        self._logger.addHandler(logHandler)

        # Load data
        with open("credentials.json") as file:
            data = json.load(file)
            self._credentials = parse_obj_as(List[Credential], data["credentials"])

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def LogIn(self) -> bool:
        pass

    @abstractmethod
    def LoadUserProfile(self) -> bool:
        pass

    def SaveUserProfile(self):
        # Write data to file
        with open("user_profile.json", "w") as file:
            file.write(self._user_profile.json())
