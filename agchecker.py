import stories

class exportstories:
    def __init__(self):
        pass

stories.Story("a1","u1","11/12/2014","bla1")
print stories.Story._instances
stories.Story("a2","u2","10/11/2014","bla1")
print stories.Story._instances

for each in stories.Story:
    each.show()
