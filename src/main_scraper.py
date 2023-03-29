""" Module to test the scrapers """

import json
from typing import List

from pydantic import parse_obj_as

from configure_scraper import ConfigureScraper
from models import Credential
from selenium_scraper import SeleniumScraper

credentials: List[Credential]
# Load credentials
with open("credentials.json", encoding="utf-8") as config_file:
    data = json.load(config_file)
    credentials = parse_obj_as(List[Credential], data["credentials"])

# Instantiating config
config = ConfigureScraper()
RETRY_ATTEMPTS = config.get_retry_attempts()

# Instantiating scraper
scraper = SeleniumScraper(config)

for credential in credentials:
    scraper.set_credential(credential)
    attempt: int = 0
    while attempt < RETRY_ATTEMPTS:
        try:
            scraper.log_in()
            scraper.load_user_profile()
            scraper.save_user_profile()
            attempt = RETRY_ATTEMPTS
        except:
            print("See the log file.")
            attempt += 1
        finally:
            scraper.log_out()

del scraper
