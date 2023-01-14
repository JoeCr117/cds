
try:
    from selenium import webdriver as _webdriver
except:
    pass


class Scraper:

    LINKEDIN = 'LinkedIn'
    CHROME = 'Chrome'
    _browsers = ['Chrome']

    def __init__(self, browser_name=None, target_site=None, job_description=None, location=None) -> None:
        self._target_browser = browser_name if browser_name else None
        self._target_site = target_site if target_site else None
        self._job_description = job_description if job_description else None
        self._locaton = location if location else None
        self._driver = self.set_driver(self._target_browser) if self._target_browser else None

    def set_driver(self, browser_name):
        if browser_name is Scraper.CHROME:
            try:
                from webdriver_manager import chrome as _chrome
            except ImportError as err:
                raise err
            self._driver = _webdriver.Chrome(_chrome.ChromeDriverManager().install())
        else:
            raise f'Browser Name not in the legal list of browsers {self._browsers}'
