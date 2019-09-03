
import requests
import sys
import os
import re
from joblib import delayed, Parallel

class loadBible:
    #Must become Genesis Page 1 {1:1}...{1:2}...
    #           Exodus Page 1 {1:1}...{1:2}...
    #           ... ... ...

    #Then call into the Bible class to create a proper Bible object.  This will be returned and the loadFromInternet OBJ will be del().


    def __init__(self, version, books):
        self.__site = 'http://www.biblegateway.com'
        self.__bookDeliminator = ' Page 1 '
        self.__startText = 'Old Testament  '
        self.__listOfBooks = books

        self.__version = version.upper()
        self._alreadyExists = self.__checkExist__()

    def __checkConection__(self):
        if 'win' in sys.platform:
            cmd = 'ping 8.8.8.8'
        elif 'linux' in sys.platform:
            cmd = 'ping 8.8.8.8 -c 3'
        if not os.system(cmd):
            self._connected = True
        else:
            self._connected = False
    def loadVersion(self, saveLocal=None):
        if not self._alreadyExists:
            bibleText = self.__loadFromInternet__(saveLocal)
        else:
            bibleText = self.__loadFromMem__()
        return bibleText
    def __getABook__(self, book):
        chaps = []
        for chapter in range(0, 151):
            requestContent = requests.request('GET',self.__makeURL__(book, str(chapter+1))).content.decode()
            chapterText = re.findall(r'num">\d+.+?s\w+?>(.+)</span>.+</div>', requestContent)
            if not chapterText:
                break
            chaps.append(chapterText)
        return chaps

    def __loadFromInternet__(self, saveLocal=None):
        self.__checkConection__()
        if not(self._connected):
            return
        bibleString = self.__startText
        # allChapters = Parallel(n_jobs=66)(delayed(self.__getABook__)(book) for book in self.__listOfBooks)
        bookIndex = 0
        for book in self.__listOfBooks:
            chapters = self.__getABook__(book)
            # chapters = allChapters[bookIndex]
            bibleString += self.__bookDeliminator + book
            for chapter in range(len(chapters)):
                # requestContent = requests.request('GET',self.__makeURL__(book, str(chapter+1))).content.decode()
                # verseList = re.findall(r'num">\d+.+?s\w+?>(.+?)</span>', requestContent)
                # chapterText = re.findall(r'num">\d+.+?s\w+?>(.+)</span>.+</div>', requestContent)
                try:
                    verseList = re.sub('<[^<]+?>', '', chapters[chapter][0]).split('\xa0')
                except:
                    print(self.__makeURL__(book, str(chapter)))
                    print(chapters[chapter])
                    raise Exception("Error loading Bible")
                # subVerseList = re.findall(r'<sup class="versenum">(\d+) </sup>', requestContent)

                if(verseList):
                    verseIndex = 1
                    for verse in verseList:
                        if((verse.find('<i>') == 0) or (verse.find('<b>') == 0)):
                            continue
                        if(verse.find(chr(8197)) >= 0):
                            verse.replace(chr(8197), '')
                        if verse[-1].isdigit():
                            verse = verse[0:-2]
                        htmlGarbageList = re.findall('(<.+?>)', verse)
                        for htmlGarbage in htmlGarbageList:
                            verse = verse.replace(htmlGarbage, '')
                        bibleString += ' {' + str(chapter + 1) + ':' + str(verseIndex)+ '} ' + verse
                        verseIndex += 1
                else:
                    break
        bookIndex += 1
        if(saveLocal):
            if not (self.__saveLocalCopy__(bibleString)):
                print('Failed to Save')
        return bibleString

    def __loadFromMem__(self):
        path = self.__findPath__()
        if 'win' in sys.platform:
            file = '\\BibleText'
        elif 'linux' in sys.platform:
            file = '/BibleText'
        path = path + file + self.__version + '.bib'
        f = open(path, 'r')
        bibleText = f.read()
        f.close()
        return bibleText
    def __hasHTML__(self, string):
        m = re.match(r'<s.+?>', string)
        if(m):
            return True
        else:
            return False

    def __makeURL__(self, book, chapter, verse=None):
        if not (type(self.__version)is str and type(book)is str and type(chapter)is str):
            raise AssertionError('One of the inputs is not a string')
        book = book.replace(' ', '+')
        urlPart1 = self.__site + '/passage/?search='
        urlPart3 = '&version='
        urlPart2 = '%3A'
        if(verse):
            return urlPart1+book+'+'+chapter+urlPart2+verse+urlPart3+self.__version
        else:
            return urlPart1 + book + '+' + chapter + urlPart3 + self.__version
    def __saveLocalCopy__(self, bibleString):
        bSuccess = False
        path = self.__findPath__()
        if 'win' in sys.platform:
            file = '\\BibleText'
        elif 'linux' in sys.platform:
            file = '/BibleText'
        try:
            path = path + file + self.__version + '.bib'
            f = open(path, 'w')
            f.write(bibleString)
            f.close()
            bSuccess = True
        except:
            pass
        return bSuccess

    def __findPath__(self):
        path = os.path.expanduser('~')
        if(sys.platform.find('linux') >= 0):
            path += '/.bibleApp'
        elif(sys.platform.find('win') >= 0):
            path += '\\AppData\\Local\\BibleApp'
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def __checkExist__(self):
        bExists = False

        path = self.__findPath__()

        for file in os.listdir(path):
            if file.find('BibleText'+self.__version+'.bib') >= 0:
                bExists = True
                break
        return bExists
