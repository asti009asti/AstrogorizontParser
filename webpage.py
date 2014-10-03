from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time
import config
import stories
import sys
import datetime

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

    def __init__(self, url, days):
        Webpage.__init__(self, url)
        self.currentpage = 1
        self.page_switch_flag = 0
        self.days = days
        self.continue_scan = True

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
            datetext = "/".join((date.text.lstrip()).split(" "))
            if self.is_date_valid(datetext):
                stories.Story(header.text, datetext, description.text[:-10])
            else:
                self.continue_scan = False
                break

    def update_current_page(self):
        self.currentpage += 1

    def nextpage(self):
        if self.currentpage == 11 and self.page_switch_flag == 0:
            self.currentpage = 3
            self.page_switch_flag = 1
        elif self.page_switch_flag > 0 and self.currentpage == 13:
            self.currentpage = 3
        nextpage_xpath = config.AG_NEXTPAGES[:-2]+ str(self.currentpage) + "]"
        for i in range(4):
            try:
                next_page_link = self.driver.find_element_by_xpath(nextpage_xpath)
            except Exceptions.NoSuchElementException:
                print "Exception!"
                time.sleep(1)
        next_page_link.click()
        self.update_current_page()

    def is_date_valid(self, param):
        date = param.split("/")
        day = int(date[0])
        month = int(date[1])
        year = int("20"+date[2])
        storydate = datetime.date(year, month, day)
        todaydate = datetime.date.today()
        if (todaydate - storydate).days < self.days:
            return True
        return False


class GWebPage(Webpage):

    def __init__(self, url):
        Webpage.__init__(self, url)
        self.domain = config.G_SEARCHDOMAIN
        self.pages = config.G_SEARCHPAGES

    def search(self, story_header):
        searchbox = self.driver.find_element_by_id(config.G_SEARCH)
        searchbox.click()
        searchbox.clear()
        searchbox.send_keys(story_header)
        searchbox.send_keys(Keys.RETURN)

    def scan(self):
        domains = self.driver.find_elements_by_xpath(config.G_DOMAINS)
        count = 0
        for each in domains:
            if self.domain in each.text:
                count += 1
        return count

    def next_page(self):
        self.driver.find_element_by_xpath(config.G_NEXTPAGE).click()
