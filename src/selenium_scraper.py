""" This module is a concrete scraper implementation with Selenium """
import json

from pydantic import parse_obj_as
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from abstract_scraper import AbstractScraper
from configure_scraper import ConfigureScraper
from models import UserProfile
from state_enum import StateEnum


class SeleniumScraper(AbstractScraper):
    """
    SeleniumScraper implements the AbstractScraper with the methods:
        __init__
        __del__
        log_in
        log_out
        load_user_profile
    """

    _scraper: WebDriver
    _current_url_page: str

    def __init__(self, config: ConfigureScraper):
        super().__init__(config)
        options = Options()
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self._scraper = webdriver.Chrome(service=service, options=options)
        self._logger.log_info("Init", "Selenium Scraper")
        self.state = StateEnum.INITIALIZED

    def __del__(self):
        self._logger.log_info("Finish", "Selenium Scraper")
        self._scraper.close()

    def log_in(self):
        if self._credential is None:
            self._logger.log_info("LogIn", "Credential is not set.")
            raise ValueError("Credential is not set.")

        self._logger.log_info("LogIn", self._credential.username)

        try:
            self._scraper.get(self._credential.url)
            self._current_url_page = self._scraper.current_url
            username_in_box = WebDriverWait(self._scraper, 10).until(
                EC.visibility_of_element_located((By.ID, "login_username"))
            )
            username_in_box.send_keys(self._credential.username)
            username_in_box.submit()
            passwd_in_box = WebDriverWait(self._scraper, 5).until(
                EC.visibility_of_element_located((By.ID, "login_password"))
            )
            passwd_in_box.send_keys(self._credential.password)
            passwd_in_box.submit()
        except (NoSuchElementException, TimeoutException) as exception:
            self._logger.log_error(
                self.state,
                "LogIn",
                "Failed for user " + self._credential.username,
                exception,
            )
            self._scraper.get_screenshot_as_file(
                self.config.get_screenshot_dir()
                + self._credential.username
                + "-login.png"
            )
            raise exception
        finally:
            self.state = StateEnum.LOGINTO

    def log_out(self):
        self._logger.log_info("LogOut", self._credential.username)
        try:
            # The get method doesn't work, it must be a POST httl request
            # self._scraper.get("https://www.upwork.com/ab/account-security/logout")
            self._scraper.execute_script(
                """
                var http = new XMLHttpRequest();
                var url = 'https://www.upwork.com/ab/account-security/logout';
                http.open('POST', url, true);
                http.send('')
                """
            )
        except (NoSuchElementException, TimeoutException) as exception:
            self._logger.log_error(
                self.state,
                "LogOut",
                "Failed for user " + self._credential.username,
                exception,
            )
            self._scraper.get_screenshot_as_file(
                self.config.get_screenshot_dir()
                + self._credential.username
                + "-logout.png"
            )
        finally:
            self.state = StateEnum.LOGOUT

    def _wait_redirect(self):
        wait_profile = WebDriverWait(self._scraper, 10)
        wait_profile.until(lambda driver: driver.current_url != self._current_url_page)

    def load_user_profile(self):
        self._logger.log_info("LoadUserProfile", self._credential.username)
        try:
            self._wait_redirect()

            self._scraper.get(
                "https://www.upwork.com/ab/create-profile/api/min/v1/welcome"
            )
            body_text = self._scraper.find_element(By.TAG_NAME, "body").text
            self._user_profile = parse_obj_as(UserProfile, json.loads(body_text))
        except (NoSuchElementException, TimeoutException) as exception:
            self._logger.log_error(
                self.state,
                "LoadUserProfile",
                "Failed for user " + self._credential.username,
                exception,
            )
            self._scraper.get_screenshot_as_file(
                self.config.get_screenshot_dir()
                + self._credential.username
                + "-load_user_profile.png"
            )
            raise exception
        finally:
            self.state = StateEnum.LOADED_PROFILE
