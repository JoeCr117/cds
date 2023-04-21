from ..sites.site import Site


class SearchPkg:
    """Package of Sites to run scraping on.
    """
    config = []

    def add_Item(self, searchConfig: "Site"):
        self.config.append(searchConfig)
