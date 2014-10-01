import stories
import webpage
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time

wbpg = webpage.Webpage("http://www.astrogorizont.com/content/ch-2")
wbpg.open()
#wbpg.scan("blabla")

headers_xpath = "//table/tbody/tr/td/h1"
dates_xpath = "//td[@bgcolor='#474E63'][span[@class='datarticles']]"
description_xpath = "//td[@colspan='2'][@valign='top']"



