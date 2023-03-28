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
from models import UserProfile


class SeleniumScraper(AbstractScraper):
    """
    SeleniumScraper implements the AbstractScraper with the methods:
        __init__
        __del__
        LogIn
        LoadUserProfile
    """

    _scraper: WebDriver

    def __init__(self):
        super().__init__()
        options = Options()
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self._scraper = webdriver.Chrome(service=service, options=options)
        self._logger.info("Starting Selenium Scraper")

    def __del__(self):
        self._scraper.close()
        self._logger.info("Done Selenium Scraper")

    def log_in(self) -> bool:
        login_attempts = 0
        for credential in self._credentials:
            login_attempts += 1
            try:
                self._scraper.get(credential.url)
                username_in_box = WebDriverWait(self._scraper, 10).until(
                    EC.visibility_of_element_located((By.ID, "login_username"))
                )
                username_in_box.send_keys(credential.username)
                username_in_box.submit()
                passwd_in_box = WebDriverWait(self._scraper, 5).until(
                    EC.visibility_of_element_located((By.ID, "login_password"))
                )
                passwd_in_box.send_keys(credential.password)
                passwd_in_box.submit()
                break
            except (NoSuchElementException, TimeoutException) as ex:
                self._scraper.get_screenshot_as_file("log/screenshots/login.png")
                msg = (
                    "LogIn: useranme '"
                    + credential.username
                    + "' failed with the following exception:\n"
                )
                msg += str(ex)
                self._logger.error(msg)
        if login_attempts == len(self._credentials):
            self._logger.fatal(
                "LogIn: We couldn't log into the system. Please try again or \
                    provide a new credential."
            )
            return False
        return True

    def _wait_redirect(self):
        old_url = self._scraper.current_url
        wait_profile = WebDriverWait(self._scraper, 10)
        wait_profile.until(lambda driver: driver.current_url != old_url)

    def load_user_profile(self) -> bool:
        try:
            self._wait_redirect()

            self._scraper.get(
                "https://www.upwork.com/ab/create-profile/api/min/v1/welcome"
            )
            body_text = self._scraper.find_element(By.TAG_NAME, "body").text
            self._user_profile = parse_obj_as(UserProfile, json.loads(body_text))
        except (NoSuchElementException, TimeoutException) as ex:
            self._logger.fatal("LoadUserProfile: %s", str(ex))
            self._scraper.get_screenshot_as_file(
                "log/screenshots/load_user_profile.png"
            )
            return False
        return True
