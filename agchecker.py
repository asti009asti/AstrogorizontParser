import stories
import webpage
import filelib
import logging

### starting log file configuration
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%y %H:%M', filename='execution.log', level=logging.INFO, filemode='w')


### Scan Astrogorizon.com stories
logging.info("1. Launching Astrogorizont.com")
webpg = webpage.AgWebPage.open("http://www.astrogorizont.com/content/ch-2", 'firefox')

logging.info("Start: Stories scan")
while webpg.continue_scan:
    webpg.scan()
    webpg.nextpage()
#stories.Story.showall()

webpg.close()
logging.info("End: Stories scan complete!")

### Search stories in Google.com
logging.info("3. Launching google.com")
gwebpg = webpage.GWebPage.open("http://www.google.com", 'firefox')

logging.info("Start: Starting stories search")
for story in stories.Story:
    gwebpg.wait_for_url_change(lambda: gwebpg.search(story))

gwebpg.close()
logging.info("End: Stories search complete!")

### Export stories and search results to a file
logging.info("4. Starting stories export to file")
if not filelib.Reporting.check_file_exists("report.txt"):
    filelib.Reporting.create_file("report.txt")
    logging.info("Start: Creating file...")
else:
    filelib.Reporting.clear_file("report.txt")
    logging.info("Start: Clearing the existing file...")

for story in stories.Story:
    filelib.Reporting.export_results_to_file("report.txt", story.csv(False))
logging.info("End: File export complete")




