import copy
from abc import ABC
from abc import abstractmethod

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
    def scrape(self, driver: Chrome | Firefox):
        pass
