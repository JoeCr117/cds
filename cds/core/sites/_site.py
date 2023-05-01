import copy as copy
from abc import ABC as ABC
from abc import abstractmethod as abstractmethod

from selenium import webdriver
from selenium.webdriver import Chrome, Firefox


class _Site(ABC):
    def __init__(self, address=None, **kwargs):
        self.address = address
        self.__dict__.update(kwargs)

    def get_settings(self) -> dict:
        settings = copy.deepcopy(self.__dict__)
        settings.pop("address")
        return settings

    @abstractmethod
    def scrape(self, scraper: Chrome | Firefox):
        pass
