import datetime

class Iteration(type):
    def __iter__(cls):
        return iter(cls._instances)

class Story:

    __metaclass__ = Iteration
    _instances = []
    _id = 1

    def __init__(self, header=None, url=None, date=None, text=None):
        """dateformat = dd/mm/yy"""
        self.header = header
        self.url = url
        self.setdate(date)
        self.text = text
        Story._instances.append(self)
        self.id = Story._id
        Story._id += 1

    def setdate(self, date):
        if date == None:
            self.date = None
        else:
            date = date.split("/")
            day = int(date[0])
            month = int(date[1])
            year = int(date[2])
            self.date = datetime.date(year, month, day)

    def csv(self):
        list =[]
        list.append(self.header)
        list.append(self.url)
        list.append(str(self.date.day)+"/"+str(self.date.month)+"/"+str(self.date.year))
        list.append(self.text)
        return ",".join(list)

    def xml(self):
        xml = ""
        xml = "<item>" + "\n"
        xml += "\t" + "<id>" + str(self.id) + "</id>" + "\n"
        xml += "\t" + "<title>" + "<![CDATA[" + self.header + "]]>" + "</title>" + "\n"
        xml += "\t" + "<link>" + self.url + "</link>" + "\n"
        xml += "\t" + "<pubDate>" + str(self.date.day)+"/"+str(self.date.month)+"/"+str(self.date.year) + "</pubDate>" + "\n"
        xml += "\t" + "<description>" + "<![CDATA[" + self.text + "]]>" + "</description>" + "\n"
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

    def show(self):
        print "story id: ", self.id
        print "Header:", self.header
        print "Date: {}/{}/{}".format(self.date.day, self.date.month, self.date.year)
        print "URL:", self.url
        print "Text:", self.text

    def __del__(self):
        pass
