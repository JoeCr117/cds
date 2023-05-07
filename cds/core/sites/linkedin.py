from ._site import _Site

import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

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
        driver.get(self.address)
        count = 0
        #This is the selection of job/location/salary/company/etc. section
        #This will find all the interactable elements and 'select them'/'type in them'
        #   as configured in the intialization of the object.






        #This is the scroll down and 'See more jobs' button press section
        #This will loop till all the target link seen limit is reached
        while self.count>count:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            a = soup.find("ul", {"class": "jobs-search__results-list"}) \
                    .find_all("a", {"class": "base-card__full-link"}, href=True)
            count = len(a)
            time.sleep(.75)
            curr_pos = driver.execute_script('return window.pageYOffset + window.innerHeight')
            page_height = driver.execute_script('return document.body.scrollHeight')
            if(curr_pos == page_height):
                driver.find_element(By.XPATH, "//button[normalize-space()='See more jobs']").click()

        return [link['href'] for link in a], "Log Empty...for now!"
