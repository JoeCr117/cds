from selenium import webdriver
from selenium.webdriver import Chrome, Firefox

from ._site import _Site

__all__ = ["LinkedIn"]


class LinkedIn(_Site):
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
        **kwargs,
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

    def scrape(self, scraper):
        print(f"Scrapper running in {__name__}")
        scraper.get(self.address)
        print(scraper.page_source)
