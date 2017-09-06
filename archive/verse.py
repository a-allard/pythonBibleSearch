class verse:
    """A class to split each verse into.  Not sure if this is really needed."""
    numWords=0
    def __init__(self):
        pass
class chapter(verse):
    """This is fun"""
    numVerses=0
    
    def __init__(self):
        verse.__init__()
class book(chapter):
    
    numChapters=0
    def __init__(self):
        pass
