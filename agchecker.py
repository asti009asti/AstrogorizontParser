import stories

class agchecker:
    def __init__(self, website, period):
        self.period = period
        self.url = website

    def parse(self):
        pass

agchecker("http://astrogorizont.com", 3).parse()

for each in stories.Story:
    each.search("http://google.com", 3).search()
