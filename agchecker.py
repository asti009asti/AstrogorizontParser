import stories
import webpage
import filelib
import logging

### starting log file configuration
logging.basicConfig(filename='execution.log', level=logging.INFO)

### Scan Astrogorizon.com stories
logging.info("launching Astrogorizont.com")
webpg = webpage.AgWebPage("http://www.astrogorizont.com/content/ch-2", 30)
webpg.launch_chrome()
webpg.open()

logging.info("Starting stories scan")
while webpg.continue_scan:
    webpg.scan()
    webpg.nextpage()
#stories.Story.showall()

webpg.close()
logging.info("stories scan complete")

### Search stories in Google.com
logging.info("Starting google.com")
gwebpg = webpage.GWebPage("http://www.google.com")
gwebpg.launch_chrome()
gwebpg.open()

logging.info("Starting stories search")
for each in stories.Story:
    gwebpg.wait_for_url_change(lambda: gwebpg.search(each))

gwebpg.close()
logging.info("Search complete!")

### Export stories and search results to a file
logging.info("Starting stories export to file")
if not filelib.Reporting.check_file_exists("report.txt"):
    filelib.Reporting.create_file("report.txt")
else:
    filelib.Reporting.clear_file("report.txt")

for each in stories.Story:
    print each.csv(False)
    filelib.Reporting.export_results_to_file("report.txt", each.csv(False))
logging.info("File export complete")




