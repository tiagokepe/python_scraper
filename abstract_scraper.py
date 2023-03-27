import json
import logging
import logging.handlers as handlers
import time
from abc import ABC, abstractmethod
from models import Credentials
from models import UserProfile

class AbstractScraper(ABC):
    _scraper = None
    _credentials = []
    _logger = None
    _user_profile: UserProfile
    
    @abstractmethod
    def __init__(self):
        self._logger = logging.getLogger('log/scraper.log')
        self._logger.setLevel(logging.DEBUG)
        logHandler = handlers.TimedRotatingFileHandler('log/scraper.log', when='D', interval=1)
        logHandler.setLevel(logging.DEBUG)
        self._logger.addHandler(logHandler)
        
        json_file = open('credentials.json')
        json_credentials = json.load(json_file)
        json_file.close()
        for cred_data in json_credentials['credentials']:
            self._credentials.append(Credentials(**cred_data))
            
    @abstractmethod
    def __del__(self):
       pass

    @abstractmethod
    def LogIn(self):
        pass
    
    @abstractmethod
    def LoadUserProfile(self):
        pass

    @abstractmethod
    def SaveUserProfile(self):
        # Write data to file
        with open('user_profile.json', 'w') as file:
            file.write(self._user_profile.json())