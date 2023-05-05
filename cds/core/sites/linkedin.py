from ._site import _Site

import time
from bs4 import BeautifulSoup

__all__ = ["LinkedIn"]


class LinkedIn(_Site):
    def __init__(
        self,
        search=None,
        count=1,
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
        self.count = count
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

    def scrape(self, driver):
        # Source: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        def infinite_scroll():
            pause = 0.01
            i = 1
            last_height = driver.execute_script("return document.body.scrollHeight")
            print(f"last height: {last_height}")
            while i < 500:
                # Wait to load page
                time.sleep(pause)
                # Scroll down to bottom
                driver.execute_script("window.scrollBy(0, 100);")
                # Wait to load page
                time.sleep(pause)
                i += 1
                # break
                # Calculate new scroll height and compare with last scroll height
                # new_height = driver.execute_script("return document.body.scrollHeight")

        driver.get(self.address)
        # Wait to load page
        time.sleep(1)
        infinite_scroll()
        print("SCROLL OVER")
        time.sleep(1)
        # print(driver.page_source)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        ul = soup.find("ul", {"class": "jobs-search__results-list"})
        return ul, "test"
        # print(f"Scrapper running in {__name__}")
        # driver.get(self.address)
        # time.sleep(300)

        # for _ in range(20):
        #     driver.find_element(By.CLASS_NAME, "base-serp-page")
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # print(driver.page_source)
        # driver.get(self.address)
        listing_count = 0
        pause = 0.01
        while listing_count < self.count:
            # Wait to load page
            time.sleep(pause)
            # Scroll down to bottom
            driver.execute_script("window.scrollBy(0, 100);")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            print(soup)
