"""
Top level Scraping Module containing the Scraper, Sites and Configurations
"""
from .search_pkg import SearchPkg


class Scraper:
    CHROME = "Chrome"
    FIREFOX = "FireFox"

    def __init__(
        self, browser=None, incognito=True, headless=None, verbose=None
    ) -> None:
        self._browser = browser if browser else None
        self._headless = headless if headless else None
        self._verbose = verbose if verbose else None
        self._search_pkg = None
        self._incognito = incognito

    def set_Pkg(self, search_pkg: "SearchPkg"):
        self._search_pkg = search_pkg

    def run(self):
        self._search_pkg.run()
