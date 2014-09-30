from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time

class webpage:

    def __init__(self, url):
        self.url = url
        self.chromeoptions = Options()
        self.chromeoptions.add_argument('--disable-extensions')
        self.chromeoptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        self.driver = webdriver.Chrome(chrome_options=self.chromeoptions)
        self.driver.get(self.url)
        self.driver.maximize_window()

    def wait_for_url_change(self, function_to_execute):
        url_before = self.driver.current_url
        function_to_execute()
        while not self.did_url_change(url_before, self.driver.current_url):
            time.sleep(5)

    def did_url_change(self, url_old, url_new):
        if url_old == url_new:
            return False
        else:
            return True

    def navigate(self, control):
        control.click()

    def scan(self, pattern):
        if "google" in self.url:
            self.scan_google(pattern)
        elif "astrogorizont" in self.url:
            self.scan_astrogorizont()

    def scan_google(self, pattern):
        pass

    def scan_astrogorizont(self, pattern):
        pattern_array = pattern.split(",")
        bytype = pattern_array[0]


        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((bytype, value)))
            self.driver.find_elements(bytype, value)
        except Exceptions.NoSuchElementException, e:
            return False
        return True