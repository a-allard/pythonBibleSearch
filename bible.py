import re
import os
import sys

class verse:
    """A class to split each verse into.  Not sure if this is really needed."""
    verses=[]
    def __init__(self):
        pass
    def load(self,text):
        print(text[0])
        text=text.replace('}','').split('{')
        for i in range(len(text)):
            self.verses.append(text[i])
        return self.verses



class chapter(verse):
    """This is fun"""
    numChapters=0
    
    _numVerses=0
    _startOfChapterKey=':1}'
    chapterText=[]
    
    def __init__(self):
        self.verse=verse()
    def load(self,bookText):
        startOfChapters=[]
        chapters=re.findall('\{\d:\d}',bookText)[-1]
        
        self.numChapters=int(re.search('\d',chapters).group())
        for curChap in range(self.numChapters):
            stringOfStart='\{'+str(curChap)+self._startOfChapterKey
            
            match=re.search(stringOfStart,bookText)
            if(match):
                startOfChapters.append(match.start()+len(stringOfStart))
        
        for i in range(len(startOfChapters)-1):
            self.chapterText.append(self.verse.load(bookText[startOfChapters[i]:startOfChapters[i+1]]))
        #self.chapterText.append(self.verse.load(bookText[startOfChapters[-1]:]))
        
        return self.chapterText
    def __get__(self,index):
        return self.chapterText[index]

    
class book(chapter):
    _startOfBookKey='Page \d+ '
    _oldTBooks=[]
    _newTBooks=[]
    books=None
    bookText=[]
    def __init__(self):
        self.chapter=chapter()

    def load(self,bibleText,match):
        startOfText=match.start()
        text=bibleText[startOfText:]

        startOfBooks=[]
        if(self.books==None):
            self.__loadBooks__()
        for curBook in self.books:
            stringOfStart=self._startOfBookKey+curBook
            match=re.search(stringOfStart,text)
            if(match):
                startOfBooks.append(match.start()+len(stringOfStart))
            else:
                print(curBook)
        #print((startOfBooks))
        for i in range(len(startOfBooks)-1):
            temp=(self.chapter.load(text[startOfBooks[i]:startOfBooks[i+1]]))
            self.bookText.append(temp)
            #print(self.books[i])
        self.bookText.append(self.chapter.load(text[startOfBooks[-1]:]))
        return self.bookText
            
    
    def __get__(self,key):
        pass
    def __findBook__(self,abrev):
        for bookName in self.books:
            match=re.search(abrev,bookName)
            if(match):
                break
        pos=self.index(bookName)
        return (bookName,pos)

    def __loadBooks__(self):
        self.books=[];
        f=open(os.path.abspath('oldTestBooks.txt'))
        for line in f:
            line=line.strip('\n')
            self._oldTBooks.append(line)
            self.books.append(line)
        f.close()
        f=open(os.path.abspath('newTestBooks.txt'))
        for line in f:
            line=line.strip('\n')
            self._newTBooks.append(line)
            self.books.append(line)
        f.close()


        
class bible(book):
    _startText='Old Testament'

    books=None;
    
    def __init__(self):
        self.book=book()

    def load(self):
        f=open('KJV_txt_ForPythonBreakupNoHeader.txt')
        bibleText=f.read()
        match=re.search(self._startText,bibleText)
        if(match):
            self.books=self.book.load(bibleText,match)
        else:
            return -1;



