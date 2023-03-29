""" Module to test the selenium scraper """
import pytest

from configure_scraper import ConfigureScraper
from models import Credential
from selenium_scraper import SeleniumScraper
from state_enum import StateEnum


class Scraper:
    """Singleton Scraper class required because of pytest doesn't handle
        inheritance instantiation properly.
    Returns:
        SeleniumScraper: singleton SeleniumScraper instance
    """

    _instance: SeleniumScraper = None  # type: ignore

    def __new__(cls):
        if cls._instance is None:
            config = ConfigureScraper()
            cls._instance = SeleniumScraper(config)
            assert cls._instance.state == StateEnum.INITIALIZED
        return cls._instance


@pytest.fixture(autouse=True)
def scraper():
    _scraper = Scraper()
    return _scraper


@pytest.mark.smoke
def test_login(scraper):
    assert scraper is not None
    credential = Credential(
        username="recruitment+scanners@argyle.com",
        password="ArgyleAwesome!@",
        secret="",
        url="https://www.upwork.com/ab/account-security/login",
    )
    scraper.set_credential(credential)
    scraper.log_in()
    assert scraper.state == StateEnum.LOGINTO


@pytest.mark.smoke
def test_load_profile(scraper):
    assert scraper is not None
    scraper.load_user_profile()
    assert scraper.state == StateEnum.LOADED_PROFILE


@pytest.mark.smoke
def test_log_out(scraper):
    assert scraper is not None
    scraper.log_out()
    assert scraper.state == StateEnum.LOGOUT
