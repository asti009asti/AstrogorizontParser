import datetime

class Iteration(type):
    def __iter__(cls):
        return iter(cls._instances)

class gsearch:

    __metaclass__ = Iteration
    _instances = []
    _id = 1

    def __init__(self, ):
        """dateformat = dd/mm/yy"""
        self.domain = None
        self.url = None
        self.description = None

    def add(self, domain, url, description):
        self.domain = domain
        self.url = url
        self.description = description
        gsearch._instances.append(self)
        self.id = gsearch._id
        gsearch._id += 1

    def csv(self):
        list =[]
        list.append(self.url)
        list.append(self.domain)
        list.append(self.description)
        return ",".join(list)

    def show(self):
        print "search element id: ", self.id
        print "domain:", self.domain
        print "URL:", self.url
        print "Text:", self.description

    def __del__(self):
        pass
