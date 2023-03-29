""" This module is a concrete scraper implementation with CloudScraper """

import json

import cloudscraper
from cloudscraper import CloudScraper
from cloudscraper.exceptions import CloudflareChallengeError

from abstract_scraper import AbstractScraper
from configure_scraper import ConfigureScraper
from state_enum import StateEnum


class CloudBasedScraper(AbstractScraper):
    """
    CloudBasedScraper implements the AbstractScraper with the methods:
        __init__
        __del__
        log_in
        log_out
        load_user_profile
    """

    _scraper: CloudScraper

    def __init__(self, config: ConfigureScraper):
        super().__init__(config)
        self._scraper = cloudscraper.create_scraper()
        self.state = StateEnum.INITIALIZED

    def __del__(self):
        del self._scraper

    def _log_response_status(self, status_code: int):
        exception = ValueError(
            "Get %s returned code: %s", self._credential.url, status_code
        )
        self._logger.log_error(
            self.state,
            "LogIn",
            "Failed for user " + self._credential.username,
            exception,
        )
        raise ValueError("Login")

    def log_in(self):
        try:
            response = self._scraper.get(self._credential.url)
            if response.status_code != 200:
                self._log_response_status(response.status_code)

            login_user = {
                "login": {"mode": "username", "username": self._credential.username}
            }
            response = self._scraper.post(
                self._credential.url, data=json.dumps(login_user)
            )
            if response.status_code != 200:
                self._log_response_status(response.status_code)

            login_passwd = {
                "login": {
                    "mode": "password",
                    "password": self._credential.password,
                    "username": self._credential.username,
                }
            }
            response = self._scraper.post(
                self._credential.url, data=json.dumps(login_passwd)
            )
            if response.status_code != 200:
                self._log_response_status(response.status_code)
        except (CloudflareChallengeError, ValueError) as exception:
            self._logger.log_error(
                self.state,
                "LogIn",
                "Failed for user " + self._credential.username,
                exception,
            )
            raise exception

        self.state = StateEnum.LOGINTO

    def log_out(self):
        self.state = StateEnum.LOGOUT

    def load_user_profile(self):
        self.state = StateEnum.LOADED_PROFILE
