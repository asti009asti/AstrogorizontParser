from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
from selenium.webdriver.common.keys import Keys
import time
import config
import stories
import sys
import datetime
import logging

class Webpage:

    def __init__(self, url):
        self.driver = None
        self.url = url
        self.continue_scan = True

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
        while not self.did_page_change(url_before, self.driver.current_url):
            time.sleep(5)

    def did_page_change(self, value_old, value_new):
        if value_old == value_new:
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

    def scan(self):
        headers = []
        dates = []
        description = []
        attempt = 0
        while len(headers) < config.AG_MIN_STORIES_ON_PAGE or \
                        len(dates) < config.AG_MIN_STORIES_ON_PAGE or \
                        len(description) < config.AG_MIN_STORIES_ON_PAGE:
            headers = self.driver.find_elements_by_xpath(config.AG_HEADERS_XPATH)
            dates = self.driver.find_elements_by_xpath(config.AG_DATES_XPATH)
            description = self.driver.find_elements_by_xpath(config.AG_DESCIPTION_XPATH)
            time.sleep(1)
            attempt += 1
            if attempt == config.MAX_ATTEMPTS_TO_FIND_ELEMENT*3:
                logging.warning("There is something wrong with the page - can't locate elements.")
                logging.warning("The server might be busy or your internet connection is too slow.")
                logging.warning("Please try again...")
                sys.exit(1)

        del headers[0]  # removing first extra header parsed

        # making sure number of headers matches number of dates and descriptions parsed
        if len(headers) != len(dates) or len(headers) != len(description):
            print len(headers)
            print len(dates)
            print len(description)
            logging.warning("There is something wrong with the page - could not locate all elements on the page.")
            logging.warning("The server might be busy or your internet connection is too slow.")
            logging.warning("Please try again...")
            sys.exit(1)

        for header, date, description in zip(headers, dates, description):
            datetext = "/".join((date.text.lstrip()).split(" "))
            if self.is_date_valid(datetext):
                # [:-10] below removed extra word at the end of the description
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
        nextpage_xpath = config.AG_NEXTPAGES[:-2] + str(self.currentpage) + "]"
        for attempt in range(config.MAX_ATTEMPTS_TO_FIND_ELEMENT):
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
        self.resultstats = ""

    def scan(self):
        attempt = 0
        while attempt < config.MAX_ATTEMPTS_TO_FIND_ELEMENT:
            try:
                domains = self.driver.find_elements_by_xpath(config.G_DOMAINS)
                count = 0
                for each in domains:
                    if self.domain in each.text:
                        count += 1
                return count
            except Exceptions.StaleElementReferenceException:
                attempt += 1

    def enter_story_in_searchbox(self, header):
        searchbox = self.driver.find_element_by_id(config.G_SEARCH)
        searchbox.click()
        searchbox.clear()
        searchbox.send_keys(header)
        searchbox.submit()
        searchbox.send_keys(Keys.RETURN)

    def next_page_exists(self, tries):
        attempts = 0
        while attempts < tries:
            try:
                self.driver.find_element(By.ID, config.G_NEXTPAGE)
                return True
            except Exceptions.NoSuchElementException:
                logging.warning("No next page! No such element")
                attempts += 1
            except Exceptions.TimeoutException:
                attempts += 1
                logging.warning("No next page! Timeout exception")
        return False

    def search(self, story):
        logging.info("Searching story")
        self.enter_story_in_searchbox(story.header)
        while not self.wait_for_page_load():
            time.sleep(1)
        for page in range(self.pages):
            logging.debug("Next page")
            if page != 0:
                while not self.wait_for_page_load():
                    time.sleep(1)
            story.search_occurences += self.scan()
            if page != self.pages-1 and self.pages != 1:
                # omit next page click for last page and if only one page is being inspected for each query
                if not self.next_page():
                    logging.debug("next page link does not exist")
                    break
            logging.debug("Next page clicked.")

    def wait_for_page_load(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,config.G_RESULTTEXT)))
        new_resultstats = self.driver.find_element_by_id(config.G_RESULTTEXT).text
        if self.resultstats != new_resultstats:
            self.resultstats = new_resultstats
            return True
        return False

    def next_page(self):
        attempt = 0
        while attempt < config.MAX_ATTEMPTS_TO_FIND_ELEMENT:
            try:
                next_page_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,config.G_NEXTPAGE)))
                next_page_link = self.driver.find_element(By.ID, config.G_NEXTPAGE)
                #webdriver.ActionChains(self.driver).move_to_element(next_page_link).click().perform()
                next_page_link.click()
                return True
            except Exception:
                time.sleep(1)
                logging.warning("Next page link is missing.")
                attempt += 1
        return False





