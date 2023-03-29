""" This module provides the scraper log class """
import logging
from logging import Logger, handlers

from state_enum import StateEnum


class LogScraper:
    """This class is responsible for logging"""

    _logger: Logger

    def __init__(self, log_filename: str):
        self._logger = logging.getLogger(log_filename)
        self._logger.setLevel(logging.DEBUG)
        log_handler = handlers.TimedRotatingFileHandler(
            "log/scraper.log", when="D", interval=1
        )
        log_handler.setLevel(logging.DEBUG)
        self._logger.addHandler(log_handler)

    def log_info(self, method_name: str, msg: str):
        """Log information

        Args:
            method_name (str): the method name is logging the information
            msg (str): the message to log
        """
        self._logger.info("%s: %s", method_name, msg)

    def log_error(self, state: StateEnum, method_name: str, msg: str, ex: Exception):
        """Log Errors

        Args:
            state (StateEnum): the scraper state
            method_name (str): the method name is logging the information
            msg (str): the message to log
            ex (Exception): the exception
        """
        self._logger.info(
            "State(%d) -> %s: %s with the following exception:",
            state.value,
            method_name,
            msg,
        )
        if ex is not None:
            self._logger.error(ex)
