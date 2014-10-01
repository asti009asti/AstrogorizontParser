import stories
import webpage
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time

webpg = webpage.Webpage("http://www.astrogorizont.com/content/ch-2")
webpg.open()
#wbpg.scan("blabla")


webpg.close()


