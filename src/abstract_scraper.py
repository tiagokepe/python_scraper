""" This module provides an abstract class used as interface to concrete classes"""
from abc import ABC, abstractmethod

from configure_scraper import ConfigureScraper
from log_scraper import LogScraper
from models import Credential, UserProfile
from state_enum import StateEnum


class AbstractScraper(ABC):
    """
    AbstractScraper provides a common interface for scrapers such as:
    - log_in
    - load_user_profile
    It also provides common methods tha derived scrapers can inherit.
    """

    state: StateEnum = StateEnum.STATELESS
    config: ConfigureScraper
    _credential: Credential
    _logger: LogScraper
    _user_profile: UserProfile

    @abstractmethod
    def __init__(self, conf: ConfigureScraper):
        self.config = conf
        self._logger = LogScraper(conf.get_log_filename())

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def log_in(self):
        """This method is called to log into the page

        Returns:
            bool: indicates successful to log into the page
        """

    @abstractmethod
    def log_out(self):
        """This method is called to log out the page

        Returns:
            bool: indicates successful to log out the page
        """

    @abstractmethod
    def load_user_profile(self):
        """This method is called to lod user profile

        Returns:
            bool: indicates successful to load user profile
        """

    def save_user_profile(self):
        """This method saves loaded user profile to a json file"""
        self._logger.log_info("SaveUserProfile", self._credential.username)
        # Write data to file
        user_file_name = "user_profiles/" + self._credential.username + ".json"
        with open(user_file_name, "w", encoding="utf-8") as file:
            file.write(self._user_profile.json())

    def set_credential(self, new_credential):
        """Set the credential to scrape the page

        Args:
            new_credential (Credetial):
        """
        self._credential = new_credential
