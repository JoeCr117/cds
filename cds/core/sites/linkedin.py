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
        scroll_attempts = 0
        sleep_time = 1
        jitter_distance = 250
        #This is the selection of job/location/salary/company/etc. section
        #This will find all the interactable elements and 'select them'/'type in them'
        #   as configured in the intialization of the object.
        if self.search is not None:
            driver.find_element(By.XPATH,"//input[@id='job-search-bar-keywords']").send_keys(f"{self.search}")
        if self.location_a is not None:
            driver.find_element(By.XPATH,"//input[@id='job-search-bar-location']").clear()
            driver.find_element(By.XPATH,"//input[@id='job-search-bar-location']").send_keys(f"{self.location_a}")
        driver.find_element(By.XPATH, "//button[@data-tracking-control-name='public_jobs_jobs-search-bar_base-search-bar-search-submit']").click()
        sleep(sleep_time)



        # TODO: Log everything!
        #This is the scroll down and 'See more jobs' button press section
        #This will loop till all the target link seen limit is reached
        #   or if the attempt limit is reached
        while scroll_attempts < 5:
            # Check if we have all the links we want
            soup = BeautifulSoup(driver.page_source, "html.parser")
            a = soup.find("ul", {"class": "jobs-search__results-list"}) \
                    .find_all("a", {"class": "base-card__full-link"}, href=True)
            if len(a)>=self.count:
                break
            # We need more links
            # Go to bottom and jitter
            driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
            for _ in range(jitter_distance):
                driver.execute_script("window.scrollBy(0,-2)")
            for _ in range(jitter_distance*2):
                driver.execute_script("window.scrollBy(0,1)")
            sleep(sleep_time*1.5)
            # See if something Loaded
            curr_pos = driver.execute_script('return window.scrollY + window.innerHeight')
            page_height = driver.execute_script('return document.body.scrollHeight')
            if curr_pos != page_height:
                # Page loaded more elements, reset counter
                scroll_attempts = 0
            else:
                # Nothing Loaded, attempt to press button
                try:
                    driver.find_element(By.XPATH, "//button[normalize-space()='See more jobs']").click()
                    # Button Pressed successfully
                    # Reset scroll attempt counter, wait for page load and continue
                    scroll_attempts = 0
                    sleep(sleep_time)
                    continue
                except ElementNotInteractableException as eni:
                    # Button could not be pressed
                    # Increase attempt counter and continue
                    scroll_attempts+=1
                    del(eni)
                    continue


        return [link['href'] for link in a], "Log Empty...for now!"
