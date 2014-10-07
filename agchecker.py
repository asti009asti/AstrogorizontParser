import stories
import webpage
import config
import filelib
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as Exceptions
import time

### Scan Astrogorizon.com stories
webpg = webpage.AgWebPage("http://www.astrogorizont.com/content/ch-2", 30)
webpg.launch_chrome()
webpg.open()

while webpg.continue_scan:
    webpg.scan()
    webpg.nextpage()
#stories.Story.showall()

webpg.close()

### Search stories in Google.com
gwebpg = webpage.GWebPage("http://www.google.com")
gwebpg.launch_chrome()
gwebpg.open()

for each in stories.Story:
    gwebpg.wait_for_url_change(lambda: gwebpg.search(each))

gwebpg.close()

### Export stories and search results to a file
if not filelib.Reporting.check_file_exists("report.txt"):
    filelib.Reporting.create_file("report.txt")
else:
    filelib.Reporting.clear_file("report.txt")

for each in stories.Story:
    print each.csv(False)
    filelib.Reporting.export_results_to_file("report.txt", each.csv(False))





