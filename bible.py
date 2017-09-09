import re
import os
import sys

class Verse:
    """A class to split each verse into.  Not sure if this is really needed."""
    
    def __init__(self):
        self.verse=[]
    def load(self,text):
        #print(text[0:100])
        text=text.replace('}','').split('{')
        for i in range(len(text)):
            self.verse.append(text[i])
        
    def __getitem__(self,key):
        return self.verse[key]
    def __setitem__(self,index,val):
        self.verse[index]=val



class Chapter:
    """This is fun"""
    
    
    _numVerses=0
    _startOfChapterKey=':1}'
    curChapter=0
    
    def __init__(self):
        self.verse=[]
        self.chapter=[]
        self.numChapters=0
    def load(self,bookText):
        startOfChapters=[]
        chapters=re.findall('\{\d+:\d+}',bookText)[-1]
        
        self.numChapters=int(re.search('{\d+',chapters).group()[1:])
        #print(self.numChapters)
        for curChap in range(self.numChapters):
            stringOfStart='\{'+str(curChap+1)+self._startOfChapterKey
            
            match=re.search(stringOfStart,bookText)
            if(match):
                startOfChapters.append(match.start()+1)
            else:
                print(curChap)
        i=0
        for i in range(len(startOfChapters)-1):
            self.chapter.append(Verse())
            
            self.chapter[i].load(bookText[startOfChapters[i]:startOfChapters[i+1]])
            
        if(i>0):
            self.chapter.append(Verse())
            self.chapter[i+1].load(bookText[startOfChapters[-1]:])
        else:
            self.chapter.append(Verse())
            self.chapter[i].load(bookText[startOfChapters[-1]:])

    def __getitem__(self,index):
        return self.chapter[index]
    def __setitem__(self,index,val):
        self.chapter[index]=val

    
class book:
    
    def __init__(self):
        _startOfBookKey='Page \d+ '
        _oldTBooks=[]
        _newTBooks=[]
        books=None
        self.book=[];
        self.lookUp={'gen':0,'genesis':0,
                     '':1,'exodus':1,
                     'lev':2,'leviticus':2}

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
        
        for i in range(len(startOfBooks)-1):
            self.book.append(Chapter())
            self.book[i].load(text[startOfBooks[i]:startOfBooks[i+1]])
            #print(self.books[i])
        self.book.append(Chapter())
        self.book[i+1].load(text[startOfBooks[-1]:])
        
            
    
    def __getitem__(self,key):
        if(isinstance(key,str)):
            try:
                index=self.loopUp[key.lower()]
            except:
                return -1
        elif(isinstance(key,int)):
            index=key
        return self.book[index]
    def __setitem__(self,index,val):
        self.book[index]=val

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
        self.bible=book()
        #return self.bible

    def load(self):
        f=open('KJV_txt_ForPythonBreakupNoHeader.txt')
        bibleText=f.read()
        match=re.search(self._startText,bibleText)
        if(match):
            
            self.bible.load(bibleText,match)
        else:
            return -1;



