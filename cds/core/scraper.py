"""
Top level Scraping Module 
"""
__all__ = ["Scraper"]
from cds.core.sites._site import _Site


class Scraper:
    CHROME = "Chrome"
    FIREFOX = "FireFox"

    def __init__(
        self, browser=None, incognito=True, headless=None, verbose=None
    ) -> None:
        self._browser = browser if browser else None
        self._headless = headless if headless else None
        self._verbose = verbose if verbose else None
        self._search_pkg = _SearchPkg()
        self._incognito = incognito

    def add_target(self, site: _Site):
        self._search_pkg.add_Item(site)

    def run(self):
        self._search_pkg.run()


class _SearchPkg:
    """Collection of Sites to run scraping on."""

    collection: list[_Site] = []

    def add_Item(self, searchConfig: "_Site"):
        self.collection.append(searchConfig)

    def run(self):
        site: "_Site"
        for site in self.collection:
            site.scrape()
