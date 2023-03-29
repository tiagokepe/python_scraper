""" This module provides the configure scraper class """
import configparser
import os
from configparser import ConfigParser
from os import path


class ConfigureScraper:
    """This class holds the configuration knobs for the scraper"""

    _config: ConfigParser
    _retry_attempts: int
    _log_filename: str
    _screenshot_dir: str

    def __init__(self):
        try:
            with open(".scraper.ini", encoding="utf-8") as config_file:
                self._config = configparser.ConfigParser()
                self._config.read_file(config_file)
                self._retry_attempts = int(
                    self._config["scraper"]["num_retry_attempts"]
                )
                self._log_filename = str(self._config["scraper"]["log_file"])
                self._screenshot_dir = str(self._config["scraper"]["screenshot_dir"])
        except:
            self._retry_attempts = 1
            self._log_filename = "scraper.log"
            self._screenshot_dir = "screenshots/"
            if path.isdir(self._screenshot_dir) is False:
                os.mkdir(self._screenshot_dir)

    def get_retry_attempts(self) -> int:
        return self._retry_attempts

    def get_log_filename(self) -> str:
        return self._log_filename

    def get_screenshot_dir(self) -> str:
        return self._screenshot_dir
