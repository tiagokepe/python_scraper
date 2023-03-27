import logging
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from models import UserProfile
from abstract_scraper import AbstractScraper
from pydantic import parse_obj_as


class SeleniumScraper(AbstractScraper):
    
    def __init__(self):
        super().__init__()
        options = Options()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        service = Service(ChromeDriverManager().install())
        self._scraper = webdriver.Chrome(service=service, options=options)
        self._logger.info("Starting Selenium Scraper")
        
    def __del__(self):
        self._scraper.close()
        self._logger.info("Done Selenium Scraper")

    def LogIn(self):
        login_attempts = 0
        for credential in self._credentials:
            login_attempts += 1
            try:
                self._scraper.get(credential.url)
                username_in_box = WebDriverWait(self._scraper, 10).until(EC.visibility_of_element_located((By.ID, 'login_username')))
                username_in_box.send_keys(credential.username)
                username_in_box.submit()
                passwd_in_box = WebDriverWait(self._scraper, 5).until(EC.visibility_of_element_located((By.ID, 'login_password')))
                passwd_in_box.send_keys(credential.password)
                passwd_in_box.submit()
                break
            except Exception as exception:
                self._scraper.get_screenshot_as_file('log/screenshots/login.png')
                msg = "LogIn: useranme '" + credential.username + "' failed with the following exception:\n"
                msg += str(exception)
                self._logger.error(msg)
        if login_attempts == len(self._credentials):
            self._logger.fatal("LogIn: We couldn't log into the system. Please try again or provide a new credential.")
            exit()

    def __WaitRedirectToProfilePage(self):
        old_url = self._scraper.current_url
        wait_profile = WebDriverWait(self._scraper, 10)
        wait_profile.until(lambda driver: driver.current_url != old_url)
        
    def LoadUserProfile(self):
        try:
            self.__WaitRedirectToProfilePage()
            
            self._scraper.get('https://www.upwork.com/ab/create-profile/api/min/v1/welcome')
            body_text = self._scraper.find_element(By.TAG_NAME, 'body').text
            profile_str = json.loads(body_text)
            self._user_profile = parse_obj_as(UserProfile, profile_str)
        except Exception as ex:
            self._logger.fatal("LoadUserProfile: " + str(ex))
            self._scraper.get_screenshot_as_file('log/screenshots/load_user_profile.png')
            exit()