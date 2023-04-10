"""
Top level Scraping Module containing the Scraper, Sites and Configurations
"""
from dataclasses import dataclass


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


class SearchPkg:
    config = []

    def add_Item(self, searchConfig: "Site"):
        self.config.append(searchConfig)


class Site:
    pass


class LinkedIn(Site):
    pass


class Indeed(Site):
    pass
