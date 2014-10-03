from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time
import config
import stories
import sys

class Webpage:

    def __init__(self, url):
        self.driver = None
        self.url = url

    def launch_chrome(self):
        self.chromeoptions = Options()
        self.chromeoptions.add_argument('--disable-extensions')
        self.chromeoptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        self.driver = webdriver.Chrome(chrome_options=self.chromeoptions)
        self.driver.maximize_window()

    def open(self):
        self.driver.get(self.url)

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

    def close(self):
        self.driver.close()


class AgWebPage(Webpage):

    def __init__(self, url):
        Webpage.__init__(self, url)
        self.currentpage = 1

    def scan(self):
        headers = []
        dates = []
        description = []
        iterations = 0
        while len(headers) < 5 or len(dates) < 5 or len(description) < 5:
            headers = self.driver.find_elements_by_xpath(config.AG_HEADERS_XPATH)
            dates = self.driver.find_elements_by_xpath(config.AG_DATES_XPATH)
            description = self.driver.find_elements_by_xpath(config.AG_DESCIPTION_XPATH)
            time.sleep(1)
            iterations += 1
            if iterations == 10:
                print "There is something wrong with the page - can't locate elements."
                print "The server might be busy or your internet connection is too slow."
                print "Please try again..."
                sys.exit(1)

        del headers[0]  # removing first extra header parsed

        if len(headers) != len(dates) or len(headers) != len(description):
            print len(headers)
            print len(dates)
            print len(description)
            print "There is something wrong with the page - could not locate all elements on the page."
            print "The server might be busy or your internet connection is too slow."
            print "Please try again..."
            sys.exit(1)

        for header, date, description in zip(headers, dates, description):
            stories.Story(header.text, "/".join((date.text.lstrip()).split(" ")), description.text[:-10])

    def update_current_page(self):
        self.currentpage += 1

    def nextpage(self):
        nextpage_xpath = config.AG_NEXTPAGES[:-2]+ str(self.currentpage) + "]"
        for i in range(4):
            try:
                next_page_link = self.driver.find_element_by_xpath(nextpage_xpath)
            except Exceptions.NoSuchElementException:
                print "Exception!"
                time.sleep(1)
        next_page_link.click()
        self.update_current_page()



class GWebPage(Webpage):
    def scan(self):
        pass