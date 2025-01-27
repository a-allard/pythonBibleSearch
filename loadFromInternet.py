
import requests
import sys
import os
import re

class loadBible:
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
            print('failed to connect.')
            return None
        self.__version=version.upper()
##        self.loadVersion()
        
        
    def __checkConection__(self):
        if not os.system('ping 8.8.8.8'):
            self._connected=True
        else:
            self._connected=False
    def loadVersion(self,saveLocal=None):
        self.__checkConection__()
        if not(self._connected):
            return
        bibleString=self.__startText
        for book in self.__listOfBooks:
            bibleString+=self.__bookDeliminator+book
            for chapter in range(1,150):
                verseList=re.findall(r'num">\d+.+?s\w+?>(.+?)</span>',requests.request('GET',self.__makeURL__(book,str(chapter))).content.decode())
                if(verseList):
                    verseIndex=1
                    for verse in verseList:
                        htmlGarbageList=re.findall('(<.+?>)',verse)
                        for htmlGarbage in htmlGarbageList:
                            verse=verse.replace(htmlGarbage,'')
                        bibleString+=' {'+str(chapter)+':'+str(verseIndex)+'} '+verse
                        verseIndex+=1
                else:
                    break;
        if(saveLocal):
            if(self.__saveLocalCopy__(bibleString))
        return bibleString


        
    def __makeURL__(self,book,chapter,verse=None):
        if not (type(self.__version)is str and type(book)is str and type(chapter)is str):
            raise AssertionError('One of the inputs is not a string')
        book=book.replace(' ','+')
        urlPart1=self.__site+'/passage/?search='
        urlPart3='&version='
        urlPart2='%3A'
        if(verse):
            return urlPart1+book+'+'+chapter+urlPart2+verse+urlPart3+self.__version
        else:
            return urlPart1+book+'+'+chapter+urlPart3+self.__version
    def __saveLocalCopy__(self,bibleString):
        bSuccess=False
        path=self.__findPath__()
        try:
            path=path+'\\BibleText'+self.__version+'.bib'
            f=open(path,'w')
            f.write(bibleString)
            f.close()
        except:
            pass
        return bSuccess

    def __findPath__(self):
        path=os.path.expanduser('~')
        if(sys.platform.find('linux')>=0):
            path+='\\.bibleApp
        elif(sys.platform.find('win')>=0):
            path+='\\AppData\\Local'
        if not os.path.exists(path):
            os.mkdir(path)
        return path




