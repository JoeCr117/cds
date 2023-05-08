from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException

from ._site import _Site

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
        sleep_time = 1
        jitter_distance = 250
        #This is the selection of job/location/salary/company/etc. section
        #This will find all the interactable elements and 'select them'/'type in them'
        #   as configured in the intialization of the object.
        if self.search is not None:
            #sleep(sleep_time)
            driver.find_element(By.XPATH,"//input[@id='job-search-bar-keywords']").send_keys(f"{self.search}")
            #sleep(sleep_time)         
        if self.location_a is not None:
            #sleep(sleep_time)
            driver.find_element(By.XPATH,"//input[@id='job-search-bar-location']").clear()
            #sleep(sleep_time)
            driver.find_element(By.XPATH,"//input[@id='job-search-bar-location']").send_keys(f"{self.location_a}")
            #sleep(sleep_time)
        driver.find_element(By.XPATH, "//button[@data-tracking-control-name='public_jobs_jobs-search-bar_base-search-bar-search-submit']").click()
        sleep(sleep_time)






        #This is the scroll down and 'See more jobs' button press section
        #This will loop till all the target link seen limit is reached
        html = driver.find_element(By.TAG_NAME, 'html')
        while self.count>count:
            html.send_keys(Keys.END)
            for _ in range(jitter_distance):
                driver.execute_script("window.scrollBy(0,-2)")
            for _ in range(jitter_distance*2):
                driver.execute_script("window.scrollBy(0,1)")
            sleep(sleep_time*1.33)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            a = soup.find("ul", {"class": "jobs-search__results-list"}) \
                    .find_all("a", {"class": "base-card__full-link"}, href=True)
            count = len(a)
            curr_pos = driver.execute_script('return window.scrollY + window.innerHeight')
            page_height = driver.execute_script('return document.body.scrollHeight')
            if(curr_pos == page_height):
                try:
                    driver.find_element(By.XPATH, "//button[normalize-space()='See more jobs']").click()
                    sleep(sleep_time)
                except ElementNotInteractableException as eni:
                    #Log this I guess
                    del(eni)

        return [link['href'] for link in a], "Log Empty...for now!"
