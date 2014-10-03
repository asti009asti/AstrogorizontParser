import datetime
import webpage


class Iteration(type):
    def __iter__(cls):
        return iter(cls._instances)

class Story:

    __metaclass__ = Iteration
    _instances = []
    _id = 1

    def __init__(self, header=None, date=None, description=None):
        """dateformat = dd/mm/yy"""
        self.header = header
        self.setdate(date)
        self.description = description
        Story._instances.append(self)
        self.id = Story._id
        Story._id += 1
        self.search_occurences = 0

    def setdate(self, date):
        if date == None:
            self.date = None
        else:
            date = date.split("/")
            day = int(date[0])
            month = int(date[1])
            year = int("20"+date[2])
            self.date = datetime.date(year, month, day)

    def csv(self):
        list =[]
        list.append(self.header)
        list.append(str(self.date.day)+"/"+str(self.date.month)+"/"+str(self.date.year))
        list.append(self.description)
        list.append(self.search_occurences)
        return ",".join(list)

    def xml(self):
        xml = ""
        xml = "<item>" + "\n"
        xml += "\t" + "<id>" + str(self.id) + "</id>" + "\n"
        xml += "\t" + "<title>" + "<![CDATA[" + self.header + "]]>" + "</title>" + "\n"
        #xml += "\t" + "<link>" + self.url + "</link>" + "\n"
        xml += "\t" + "<pubDate>" + str(self.date.day)+"/"+str(self.date.month)+"/"+str(self.date.year) + "</pubDate>" + "\n"
        xml += "\t" + "<description>" + "<![CDATA[" + self.description + "]]>" + "</description>" + "\n"
        xml += "</item>" + "\n"
        return xml

    @classmethod
    def RSS(cls):
        xml = """<?xml version="1.0" encoding="UTF-8" ?>""" + "\n"
        xml += """<rss version="2.0">""" + "\n"
        xml += "<channel>" + "\n"
        for each in cls._instances:
            xml += each.xml()
        xml += "</channel>" + "\n"
        xml += "</rss>"
        return xml

    @classmethod
    def showall(cls):
        if cls._instances == []:
            print "No stories exist so far"
        else:
            [cls.show(each) for each in cls._instances]

    def show(self):
        print "story id: ", self.id
        print "Header:", self.header
        print "Date: {}/{}/{}".format(self.date.day, self.date.month, self.date.year)
        #print "URL:", self.url
        print "Description:", self.description
        print "Search occurences:", self.search_occurences

    def search(self):
        gwebpg = webpage.GWebPage("http://www.google.com")
        gwebpg.launch_chrome()
        gwebpg.open()
        gwebpg.wait_for_url_change(lambda: gwebpg.search(self.header))

        for page in range(gwebpg.pages):
            self.search_occurences += gwebpg.scan()
            if page != gwebpg.pages-1 and gwebpg.pages != 1:
                # omit next page click for last page and if only one page is being inspected for each query
                gwebpg.wait_for_url_change(lambda: gwebpg.next_page())
        gwebpg.close()

    def __del__(self):
        pass
