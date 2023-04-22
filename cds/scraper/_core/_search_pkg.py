from .._sites._site import Site as _site


class SearchPkg:
    """Package of Sites to run scraping on."""

    config: list[_site] = []

    def add_Item(self, searchConfig: "_site"):
        self.config.append(searchConfig)

    def run(self):
        site: "_site"
        for site in self.config:
            site.scrape()
