AG_HEADERS_XPATH = "//table/tbody/tr/td/h1"  # story headers
AG_DATES_XPATH = "//td[@bgcolor='#474E63'][span[@class='datarticles']]"  # story dates
AG_DESCIPTION_XPATH = "//td[@colspan='2'][@valign='top']"  # story descriptions
AG_NEXTPAGES = "//table[14]/tbody/tr/td/span[@class='gorlin']/a[position()=1]"  # next 10 pages links
AG_CHECK_PERIOD = 30  # time period to export stories for
AG_MIN_STORIES_ON_PAGE = 5  # minimal expected number of stories to appear on astrogorizon page


G_SEARCH = "gbqfq"  # google's searchbox
#G_NEXTPAGE = "//a[@id='pnnext']/span[2]"
G_NEXTPAGE = "pnnext"  # google's next page link
G_DOMAINS = "//cite[@class='_Rm' or @class='_Rm bc']"  # google results' domains
G_RESULTTEXT = "resultStats"  # google resultStat field (probably loads last)

G_SEARCHPAGES = 3  # number of google pages to scan
G_SEARCHDOMAIN = "astrogorizont.com"  # domain to search for
MAX_ATTEMPTS_TO_FIND_ELEMENT = 3  # number of attempts to access elements via selenium