import copy as _copy
from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod


class Site(_ABC):
    def __init__(self, address=None, **kwargs):
        self.address = address
        self.__dict__.update(kwargs)

    def get_settings(self) -> dict:
        settings = _copy.deepcopy(self.__dict__)
        settings.pop("address")
        return settings

    @_abstractmethod
    def scrape(self):
        pass
