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
        self.verse=verse.__init__(self)
class book(chapter):
    _oldTBooks=[]
    _newTBooks=[]
    books=[]
    _numChapters=0
    def __init__(self):
        self.chapter=chapter.__init__(self)

    def load(self,bibleText,match):
        startOfText=match.start()
        text=bibleText[startOfText+len(match.group()):]
        
class bible(book):
    _startText='Old Testament'

    books=[];
    
    def __init__(self):
        self.book=book.__init__(self)

    def load(self):
        f=open('KJV_txt_ForPythonBreakup.txt')
        bibleText=f.read()
        match=re.search(self._startText,bibleText)
        if(match):
            self.book.load(bibleText,match)
        else:
            return -1;
