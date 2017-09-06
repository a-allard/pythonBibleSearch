import re

class verse:
    """A class to split each verse into.  Not sure if this is really needed."""
    _numWords=0
    def __init__(self):
        pass
class chapter(verse):
    """This is fun"""
    _numVerses=0
    
    def __init__(self):
        verse.__init__(self)
class book(chapter):
    
    _numChapters=0
    def __init__(self):
        chapter.__init__(self)

        
class bible(book):
    _startText='Old Testament'


    books=[];
    
    def __init__(self):
        book.__init__(self)

    def load(self):
        f=open('KJV_txt_ForPythonBreakup.txt')
        for line in f:
            match=re.search(self._startText,line)
            if not (match==None):
                break
        print(f.readline())
        f.close()
        
