
import requests
import sys
import os


class loadFromInterent:
    _site='http://www.biblegateway.com'
    def __init__(self):
        self._connected=False
    def __checkConection__(self):
        if not os.system('ping 8.8.8.8'):
            self._connected=True
        else:
            self._connected=False
    def loadVersion(self,ver):
        self.__checkConection__()
        if not(self._connected):
            return
        
