import re
import os
import sys


sys.path.insert(0,os.path.abspath(r"3901174"))
from strReferenceList import strReferenceList
import caselessDictionary

class Verse:
    """A class to split each verse into.  Not sure if this is really needed."""
    
    def __init__(self):
        self.verse=[]
    def load(self,text):
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
        self.lookUp={}
        
        self._lookUp=caselessDictionary.caselessDictionary()
        self.lookUp.update({'Gen':0,'Genesis':0,
                     'Ex':1,'Exodus':1,
                     'Lev':2,'Leviticus':2,
                     'Num':3,'Numbers':3,
                     'Deut':4,'Deuteronomy':4,
                     'Josh':5,'Joshua':5,
                     'Judg':6,'Judges':6,
                     'Ruth':7,
                     '1 Sam':8,'1 Samuel':8,
                     '2 Sam':9,'2 Samuel':9,
                     '1 Kings':10,
                     '2 Kings':11,
                     '1 Chr':12, '1 Chronicles':12,
                     '2 Chr':13, '2 Chronicles':13,
                     'Ezra':14,
                     'Neh':15,'Nehemiah':15,
                     'Esth':16,'Esther':16,
                     'Job':17,
                     'Ps':18,'Psalms':18,
                     'Prov':19,'Proverbs':19,
                     'Eccl':20,'Ecclsiastes':20,
                     'Song':21,'Song of Solomon':21,
                     'Isa':22,'Isaiah':22,
                     'Jer':23,'Jeremiah':23,
                     'Lam':24,'Lamantations':24,
                     'Ezek':25,'Ezekial':25,
                     'Dan':26,'Daniel':26,
                     'Hos':27,'Hosea':27,
                     'Joel':28,
                     'Am':29,'Amos':29,
                     'Ob':30,'Obadiah':30,
                     'Jon':31,'Jonah':31,
                     'Mic':32,'Micah':32,
                     'Nah':33,'Nahum':33,
                     'Hab':34,'Habakkuk':35,
                     'Zeph':35,'Zephaniah':35,
                     'Hag':36,'Haggai':36,
                     'Zech':37,'Zechariah':37,
                     'Mal':38,'Malachi':38,
                     'Mt':39,'Matthew':39,
                     'Mk':40,'Mark':40,
                     'Lk':41,'Luke':41,
                     'Jn':42,'John':42,
                     'Acts':43,'Acts of the Apostles':43,
                     'Rom':44,'Romans':44,
                     '1 Cor':45,'1 Corinthians':45,
                     '2 Cor':46,'2 Corinthians':46,
                     'Gal':47,'Galatians':47,
                     'Eph':48,'Ephesians':48,
                     'Phil':49,'Philippians':49,
                     'Col':50,'Colossians':50,
                     '1 Thess':51,'1 Thessalonians':51,
                     '2 Thess':52,'2 Thessalonians':52,
                     '1 Tim':53,'1 Timothy':53,
                     '2 Tim':54,'2 Timothy':54,
                     'Titus':55,
                     'Philemon':56,
                     'Heb':57,'Hebrews':57,
                     'Jas':58,'James':59,
                     '1 Pet':59,'1 Peter':59,
                     '2 Pet':60,'2 Peter':60,
                     '1 Jn':61,'1 John':61,
                     '2 Jn':62,'2 John':62,
                     '3 Jn':63,'3 John':63,
                     'Jude':64,
                     'Rev':65,'Revelation':65,'Revelations':65
                     })
        keys=list(self.lookUp.keys())
        for key in keys:
            val=self.lookUp[key]
            self._lookUp[key.lower()]=val

        self.book=strReferenceList(self.lookUp);

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
        self.book.append(Chapter())
        self.book[i+1].load(text[startOfBooks[-1]:])
        
            
    #setters and getters
    def __getitem__(self,index):
        return self.book[index]
    def __setitem__(self,index,val):
        self.book[index]=val
#Commented out to before deleting from the code.  Making sure it works without
        
##    def __findBook__(self,abrev):
##        for bookName in self.books:
##            match=re.search(abrev,bookName)
##            if(match):
##                break
##        pos=self.index(bookName)
##        return (bookName,pos)

## Loading two text files with the books of the bible in to allow the program to
## find the books of the bible 
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
    #This is the deliminator for the script to find the start of the acutal
    #text
    _startText='Old Testament'

    books=None;
    
    def __init__(self):
        self.bible=book()

    def load(self,version='kjv'):
        version=version.lower()
        if(version=='kjv'):
            f=open('KJV.txt')
        
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
            elif(isinstance(books[0],str) or isinstance(books,list)):
                if(isinstance(books,str)):
                    books=[books]
                books2=[]
                for book in books:
                    books2.append(self.bible.lookUp[book])
                books=books2
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
                        if(ver>len(self.bible.book[book].chapter[chapter].verse)-1):
                            verses2=verses2[0:verses2.index(ver)]
                            break
                for verse in verses2:
                    match=re.search(searchFor.lower(),self.bible.book[book].chapter[chapter].verse[verse].lower())
                    if(match):
                        matchList.append(match)
                        indexList.append((book,chapter,verse))
                
        return(matchList,indexList)

    def dispSearch(self, indexes):
        stats=stat()
        stats.numberOfAppearances=len(indexes)
        
        lastBookAbrv=''
        for index in indexes:
            bookAbrv=list(self.bible.lookUp.keys())[list(self.bible.lookUp.values()).index(index[0])]
            print(bookAbrv+' : '+self.bible.book[index[0]].chapter[index[1]].verse[index[2]])
            if not (lastBookAbrv==bookAbrv):
                lastBookAbrv=bookAbrv
                stats.listOfBooks.append(bookAbrv)
        return stats



class stat:
    
    def __init__(self):
        self.numberOfAppearances=0
        self.listOfBooks=[]
    


