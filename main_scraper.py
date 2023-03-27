from models import UserProfile
from selenium_scraper import SeleniumScraper

selenium_scraper = SeleniumScraper()
selenium_scraper.LogIn()
selenium_scraper.LoadUserProfile()
selenium_scraper.SaveUserProfile()

del selenium_scraper