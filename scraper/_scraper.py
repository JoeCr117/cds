"""
Top level Scraping Module containing the Scraper, Sites and Configurations
"""
from dataclasses import dataclass as _dataclass
import copy as _copy
from abc import ABC as _ABC, abstractmethod as _abstractmethod

print("fuck")


class Scraper:
    CHROME = "Chrome"
    FIREFOX = "FireFox"

    def __init__(self, browser=None, headless=None, verbose=None) -> None:
        self._browser = browser if browser else None
        self._headless = headless if headless else None
        self._verbose = verbose if verbose else None
        self._search_pkg = None

    def set_Pkg(self, search_pkg: "SearchPkg"):
        self._search_pkg = search_pkg

    def run(self):
        site: Site
        for site in self._search_pkg.config:
            site.run()


class SearchPkg:
    config = []

    def add_Item(self, searchConfig: "Site"):
        self.config.append(searchConfig)


class Site(_ABC):
    def __init__(self, *args, address=None, **kwargs):
        self.address = address
        self.__dict__.update(kwargs)

    def get_settings(self) -> dict:
        settings = _copy.deepcopy(self.__dict__)
        settings.pop("address")
        return settings

    @_abstractmethod
    def run(self):
        pass


class LinkedIn(Site):
    def __init__(
        self,
        *args,
        search=None,
        location_a=None,
        location_b=None,
        location_c=None,
        distance=None,
        sort=None,
        company=None,
        salary=None,
        job_type=None,
        experience=None,
        **kwargs
    ):
        self.search = search
        self.location_a = location_a
        self.location_b = location_b
        self.location_c = location_c
        self.distance = distance
        self.sort = sort
        self.company = company
        self.salary = salary
        self.job_type = job_type
        self.experience = experience
        super().__init__(address="https://www.linkedin.com/jobs/search", **kwargs)

    def run(self):
        pass


class Indeed(Site):
    def __init__(self, *args, search=None, location=None, **kwargs):
        self.search = search
        self.location = location
        super().__init__(address="https://www.indeed.com", **kwargs)

    def run(self):
        pass


__all__ = ["Scraper", "SearchPkg", "LinkedIn", "Indeed"]
