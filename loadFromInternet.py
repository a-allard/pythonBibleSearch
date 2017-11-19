
import requests
import sys
import os
import re

class loadFromInternet:
    #Must become Genesis Page 1 {1:1}...{1:2}...
    #           Exodus Page 1 {1:1}...{1:2}...
    #           ... ... ...

    #Then call into the Bible class to create a proper Bible object.  This will be returned and the loadFromInternet OBJ will be del().




    
    def __init__(self,version,books):
        self.__site='http://www.biblegateway.com'
        self.__bookDeliminator=' Page 1 '
        self.__startText='Old Testament  '
        self.__listOfBooks=books
        self.__checkConection__()
        if not self._connected:
            return None
        self.__version=version.upper()
        self.loadVersion()
        
        
    def __checkConection__(self):
        if not os.system('ping 8.8.8.8 -c 1'):
            self._connected=True
        else:
            self._connected=False
    def loadVersion(self):
        self.__checkConection__()
        if not(self._connected):
            return
        bibleString=self.__startText
        for book in self.__listOfBooks:
            bibleString+=self.__bookDeliminator+book
            for chapter in range(150):
                verseList=re.findall(r'num">\d+.+?s\w+?>(.+?)</span>',requests.request('GET',self.__makeURL__(book,str(chapter))).content.decode())
                verseIndex=0
                for verse in verseList:
##                    verseReturned=re.findall(r'num">\d+.+?s\w+?>(.+?)</span>',requests.request('GET',self.__makeURL__(book,str(chapter),str(verse))).content.decode())
##                    if(len(verseReturned)>0):
                        bibleString+=' {'+str(chapter)+':'+str(verseIndex)+'} '+verse
                        verseIndex+=1
        try:
            path=os.getenv('HOME')+'\\Documents\\BibleParsed.txt'
            f=open(path,'w')
            f.write(bibleString)
            f.close()
        except:
            pass
        return bibleString
        del(self)


        
    def __makeURL__(self,book,chapter,verse=None):
        if not (type(self.__version)is str and type(book)is str and type(chapter)is str):
            raise AssertionError('One of the inputs is not a string')
            
        urlPart1=self.__site+'/passage/?search='
        urlPart3='&version='
        urlPart2='%3A'
        if(verse):
            return urlPart1+book+'+'+chapter+urlPart2+verse+urlPart3+self.__version
        else:
            return urlPart1+book+'+'+chapter+urlPart3+self.__version
    


