import stories
import webpage
import filelib
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time

webpg = webpage.AgWebPage("http://www.astrogorizont.com/content/ch-2", 30)
webpg.launch_chrome()
webpg.open()

while webpg.continue_scan:
    webpg.scan()
    webpg.nextpage()
stories.Story.showall()

for each in stories.Story:
    each.search()


webpg.close()


