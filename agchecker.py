import stories
import webpage
import filelib
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time

webpg = webpage.AgWebPage("http://www.astrogorizont.com/content/ch-2")
webpg.launch_chrome()
webpg.open()

#nextpages = self.driver.find_elements_by_xpath(config.AG_NEXTPAGE)
#        for each in nextpages:

for i in range(1, 4):
    webpg.scan()
    webpg.nextpage()

stories.Story.showall()


#file = filelib.ConfigFile.read_config("config.py")

webpg.close()


