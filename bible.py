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
        self._startOfBookKey='Page \d+ '
        self._oldTBooks=[]
        self._newTBooks=[]
        self.books=None
        self.book=[];
        self.lookUp={'gen':0,'genesis':0,
                     'ex':1,'exodus':1,
                     'lev':2,'leviticus':2,
                     'num':3,'numbers':3,
                     'deut':4,'deuteronomy':4,
                     'josh':5,'joshua':5,
                     'judg':6,'judges':6,
                     'ruth':7,
                     '1 sam':8,'1 samuel':8,
                     '2 sam':9,'2 samuel':9,
                     '1 kings':10,
                     '2 kings':11,
                     '1 chr':12, '1 chronicles':12,
                     '2 chr':13, '2 chronicles':13,
                     'ezra':14,
                     'neh':15,'nehemiah':15,
                     'esth':16,'esther':16,
                     'job':17,
                     'ps':18,'psalms':18,
                     'prov':19,'proverbs':19,
                     'eccl':20,'ecclsiastes':20,
                     'song':21,'song of solomon':21,
                     'isa':22,'isaiah':22,
                     'jer':23,'jeremiah':23,
                     'lam':24,'lamantations':24,
                     'ezek':25,'ezekial':25,
                     'dan':26,'daniel':26,
                     'hos':27,'hosea':27,
                     'joel':28,
                     'am':29,'amos':29,
                     'ob':30,'obadiah':30,
                     'jon':31,'jonah':31,
                     'mic':32,'micah':32,
                     'nah':33,'nahum':33,
                     'hab':34,'habakkuk':35,
                     'zeph':35,'zephaniah':35,
                     'hag':36,'haggai':36,
                     'zech':37,'zechariah':37,
                     'mal':38,'malachi':38,
                     'mt':39,'matthew':39,
                     'mk':40,'mark':40,
                     'lk':41,'luke':41,
                     'jn':42,'john':42,
                     'acts':43,'acts of the apostles':43,
                     'rom':44,'romans':44,
                     '1 cor':45,'1 corinthians':45,
                     '2 cor':46,'2 corinthians':46,
                     'gal':47,'galatians':47,
                     'eph':48,'ephesians':48,
                     'phil':49,'philippians':49,
                     'col':50,'colossians':50,
                     '1 thess':51,'1 thessalonians':51,
                     '2 thess':52,'2 thessalonians':52,
                     '1 tim':53,'1 timothy':53,
                     '2 tim':54,'2 timothy':54,
                     'titus':55,
                     'philemon':56,
                     'heb':57,'hebrews':57,
                     'jas':58,'james':59,
                     '1 pet':59,'1 peter':59,
                     '2 pet':60,'2 peter':60,
                     '1 jn':61,'1 john':61,
                     '2 jn':62,'2 john':62,
                     '3 jn':63,'3 john':63,
                     'jude':64,
                     'rev':65,'revelation':65,'revelations':65
                     }

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


        
class bible:
    _startText='Old Testament'

    books=None;
    
    def __init__(self):
        self.bible=book()
        #return self.bible

    def load(self):
        f=open('KJV_txt_ForPythonBreakup.txt')
        bibleText=f.read()
        match=re.search(self._startText,bibleText)
        if(match):
            
            self.bible.load(bibleText,match)
        else:
            return -1
    def search(self,searchFor,books=None,chapters=None,verses=None):
        if not (books==None):
            if(isinstance(books,int)):
                books=[books]
            elif(isinstance(books[0],str)):
                if(isinstance(books,list)):
                    return
        else:
            books=list(range(66))
        if not(chapters==None):
            if(isinstance(chapters,int)):
                chapters=[chapters]
        else:
            chapters=list(range(150))
        if not(verses==None):
            if(isinstance(verses,int)):
                verses=[verses]
        else:
            verses=list(range(200))
        matchList=[]
        indexList=[]
        books=sorted(books)
        chapters=sorted(chapters)
        verses=sorted(verses)
        for book in books:
            chapters2=chapters
            if(max(chapters2)>len(self.bible.book[book].chapter)):
                for chap in chapters2:
                    if(chap>len(self.bible.book[book].chapter)-1):
                        chapters2=chapters2[0:chapters2.index(chap)]
                        break
            for chapter in chapters2:
                verses2=verses
                if(max(verses2)>len(self.bible.book[book].chapter[chapter].verse)):
                    for ver in verses2:
                        #print(ver)
                        if(ver>len(self.bible.book[book].chapter[chapter].verse)-1):
                            verses2=verses2[0:verses2.index(ver)]
                            break
                #return verses
                #print(chapter)
                for verse in verses2:
                    match=re.search(searchFor.lower(),self.bible.book[book].chapter[chapter].verse[verse].lower())
                    if(match):
                        matchList.append(match)
                        indexList.append((book,chapter,verse))
                #print(verse)
                
        return(matchList,indexList)



