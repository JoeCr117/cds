from ._site import Site

__all__ = ["Indeed"]


class Indeed(Site):
    def __init__(self, *args, search=None, location=None, **kwargs):
        self.search = search
        self.location = location
        super().__init__(address="https://www.indeed.com", **kwargs)

    def scrape(self):
        pass