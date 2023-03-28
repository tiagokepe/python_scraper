""" Module to test the scrapers """

from selenium_scraper import SeleniumScraper

selenium_scraper = SeleniumScraper()
selenium_scraper.log_in()
selenium_scraper.load_user_profile()
selenium_scraper.save_user_profile()

del selenium_scraper
