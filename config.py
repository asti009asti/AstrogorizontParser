AG_HEADERS_XPATH = "//table/tbody/tr/td/h1"  # story headers
AG_DATES_XPATH = "//td[@bgcolor='#474E63'][span[@class='datarticles']]"  # story dates
AG_DESCIPTION_XPATH = "//td[@colspan='2'][@valign='top']"  # story descriptions
AG_NEXTPAGES = "//table[14]/tbody/tr/td/span[@class='gorlin']/a[position()=1]"  # next 10 pages links
AG_PERIOD = 10  #time period to export stories for