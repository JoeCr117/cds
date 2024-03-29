from time import sleep
from typing import List, Literal

from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ._site import _Site

__all__ = ["LinkedIn"]


class LinkedIn(_Site):

    def __init__(
        self,
        search=None,
        count=1,
        location=None,
        distance:Literal[10,25,50,75,100]=None,
        salary=None,
        job_type=None,
        experience=None,
        on_site:List[Literal[1,2,3]] = None, # List of ints [1,2,3]
        **kwargs,
    ):
        self.search = search
        self.count = count
        self.location = location
        self.distance = distance
        self.salary = salary
        self.job_type = job_type
        self.experience = experience
        self.on_site = on_site
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
        # Enter a location
        if self.location is not None:
            driver.find_element(By.XPATH,"//input[@id='job-search-bar-location']").clear()
            driver.find_element(By.XPATH,"//input[@id='job-search-bar-location']").send_keys(f"{self.location}")
            driver.find_element(By.XPATH, "//button[@data-tracking-control-name='public_jobs_jobs-search-bar_base-search-bar-search-submit']").click()
            # Location searched
            if self.distance is not None:
                print('Entering distance add routine')
                driver.find_element(By.XPATH,"(//div[@class='collapsible-dropdown flex items-center relative hyphens-auto'])[2]").click()
                sleep(sleep_time*2)
                print('Clicked Drop down')
                print(f"In: {driver.title.strip()}")
                match self.distance:
                    case 10:
                        driver.find_element(By.XPATH,"//label[normalize-space()='10 mi (15km)']").click()
                    case 25:
                        driver.find_element(By.XPATH,"//label[normalize-space()='25 mi (40 km)']").click()
                    case 50:
                        driver.find_element(By.XPATH,"//label[normalize-space()='50 mi (80 km)']").click()
                    case 75:
                        driver.find_element(By.XPATH,"//label[normalize-space()='75 mi (120 km)']").click()
                    case 100:
                        driver.find_element(By.XPATH,"//label[normalize-space()='100 mi (160 km)']").click()
                sleep(sleep_time*4)
                print('Clicked Option')
                print(f"In: {driver.title.strip()}")
                driver.find_element(By.XPATH,"//button[@data-tracking-control-name='public_jobs_distance'][normalize-space()='Done']").click()
                sleep(sleep_time*4)
                print('Clicked Done')
                print(f"In: {driver.title.strip()}")    
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
                    del eni
                    continue
        return [link['href'] for link in a][:self.count], "Log Empty...for now!"
