import stories
import webpage
import filelib
import logging

### starting log file configuration
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%y %H:%M', filename='execution.log', level=logging.INFO, filemode='w')


### Scan Astrogorizon.com stories
logging.info("1. Launching Astrogorizont.com")
webpg = webpage.AgWebPage("http://www.astrogorizont.com/content/ch-2", 30)
webpg.launch_chrome()
webpg.open()

logging.info("Start: Stories scan")
while webpg.continue_scan:
    webpg.scan()
    webpg.nextpage()
#stories.Story.showall()

webpg.close()
logging.info("End: Stories scan complete!")

### Search stories in Google.com
logging.info("3. Launching google.com")
gwebpg = webpage.GWebPage("http://www.google.com")
gwebpg.launch_chrome()
gwebpg.open()

logging.info("Start: Starting stories search")
for each in stories.Story:
    gwebpg.wait_for_url_change(lambda: gwebpg.search(each))

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

for each in stories.Story:
    print each.csv(False)
    filelib.Reporting.export_results_to_file("report.txt", each.csv(False))
logging.info("End: File export complete")




