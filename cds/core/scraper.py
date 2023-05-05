"""
Top level Scraping Module 
"""
__all__ = ["Scraper"]
from typing import Literal

from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as firefox_options

from cds.core.sites._site import _Site


class Scraper:
    CHROME = "Chrome"
    FIREFOX = "Firefox"
    EDGE = "Edge"
    SUPPORTED_BROWSERS = [CHROME, FIREFOX]

    def __init__(
        self,
        browser: Literal["Chrome", "FireFox"] = None,
        headless: "bool" = False,
        verbose: "bool" = False,
    ) -> None:
        self._verbose = verbose
        if browser not in self.SUPPORTED_BROWSERS:
            raise ValueError("Browser must be defined.")
        self._driver = self._create_driver(browser, headless)
        self._search_pkg = _SearchPkg()

    def _create_driver(self, browser, headless):
        if browser is self.CHROME:
            options = chrome_options()
            # options.add_argument("--start-maximized")
            if headless:
                options.add_argument("--headless")
            return Chrome(options=options)

        elif browser is self.FIREFOX:
            options = firefox_options()
            # options.add_argument("--start-maximized")
            if headless:
                options.add_argument("--headless")
            return Firefox(options=options)
        else:
            raise ValueError(
                f"{browser} is not a legal input, legal values are [{self.CHROME},{self.FIREFOX}]"
            )

    def add_target(self, site: _Site):
        self._search_pkg.add_Item(site)

    def run(self):
        return self._search_pkg.run(self._driver)


class _SearchPkg:
    """Collection of Sites to run scraping on."""

    def __init__(self) -> None:
        self.collection: list[_Site] = []

    def add_Item(self, searchConfig: "_Site"):
        self.collection.append(searchConfig)

    def run(self, scraper: "Chrome|Firefox"):
        # This is where the concurrent or parallel exicution will go to speed up the data gathering
        data = []
        log = []
        for site in self.collection:
            new_data, new_log = site.scrape(scraper)
            data.append(new_data)
            log.append(new_log)
        # scraper.close()
        return data, log
