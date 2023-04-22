from ..sites.site import Site


class SearchPkg:
    """Package of Sites to run scraping on."""

    config: list[Site] = []

    def add_Item(self, searchConfig: "Site"):
        self.config.append(searchConfig)

    def run(self):
        site: "Site"
        for site in self.config:
            site.scrape()
