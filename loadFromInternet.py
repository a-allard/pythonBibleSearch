
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
        bibleText=self.loadVersion()
        del(self)
        return bibleText
        
    def __checkConection__(self):
        if not os.system('ping 8.8.8.8'):
            self._connected=True
        else:
            self._connected=False
    def loadVersion(self):
        self.__checkConection__()
        if not(self._connected):
            return
        bibleString=self.__startText
        for book in self.__listOfBooks:
            bibleString+=book+self.__bookDeliminator
            for chapter in range(150):
                for verse in range(200):
                    verseReturned=re.findall(r'num">\d+.+?s\w+?>(.+?)</span>',requests.request('GET',self.__makeURL__(book,str(chapter),str(verse))).content.decode())
                    if(len(verseReturned)>0):
                        bibleString+='{'+str(chapter)+':'+str(verse)+'}'+verseReturned[0]
        return bibleString


        
    def __makeURL__(self,book,chapter,verse):
        if not (type(self.__version)is str and type(book)is str and type(chapter)is str and type(verse)is str):
            raise AssertionError('One of the inputs is not a string')
            
        urlPart1=self.__site+'/passage/?search='
        urlPart3='&version='
        urlPart2='%3A'
        return urlPart1+book+'+'+chapter+urlPart2+verse+urlPart3+self.__version
    


