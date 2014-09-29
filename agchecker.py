import stories

class exportstories:
    def __init__(self):
        pass

stories.Story("story 1 header","http://blabla.bla","11/12/2014","text 1")
print stories.Story._instances
stories.Story("story 2 header","http://blabla.bla","10/11/2014","text 2")
print stories.Story._instances

print stories.Story.RSS()
