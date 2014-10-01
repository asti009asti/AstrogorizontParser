from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time

class Webpage:

    def __init__(self, url):
        self.driver = None
        self.url = url

    def launchchrome(self):
        self.chromeoptions = Options()
        self.chromeoptions.add_argument('--disable-extensions')
        self.chromeoptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        self.driver = webdriver.Chrome(chrome_options=self.chromeoptions)
        self.driver.maximize_window()


    def open(self):
        self.launchchrome()
        self.driver.get(self.url)

    def nextpage(self, element):
        element.click()

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

    def scan(self, pattern):
        if "google" in self.url:
            self.scan_google(pattern)
        elif "astrogorizont" in self.url:
            self.scan_astrogorizont(pattern)

    def scan_google(self, pattern):
        print "Google!"

    def scan_astrogorizont(self, pattern):
        print "AG!"
        headers = wbpg.driver.find_elements_by_xpath(headers_xpath)
        dates = wbpg.driver.find_elements_by_xpath(dates_xpath)
        description = wbpg.driver.find_elements_by_xpath(description_xpath)


        print headers
        del headers[0]
        print headers


        for i, each in enumerate(headers):
            print each.text

        for each in dates:
            tmp = (each.text.lstrip()).split(" ")
            #tmp = each.text.split(" ")
            print "/".join(tmp)


        for each in description:
            print each.text[:-10]

        #for header, date, description in zip(headers, dates, description):
        #    print header.text, date.text, description.text

    def __del__(self):
        self.driver.close()