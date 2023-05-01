from ._site import _Site

__all__ = ["Indeed"]


class Indeed(_Site):
    def __init__(self, *args, search=None, location=None, **kwargs):
        self.search = search
        self.location = location
        super().__init__(address="https://www.indeed.com", **kwargs)

    def scrape(self, scraper):
        print(f"Scrapper running in {__name__}")
