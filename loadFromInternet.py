
import requests
import sys
import os


class loadFromInterent:
    _site='http://www.biblegateway.com'
    def __init__(self):
        self.connected=False
    def __checkCnnection__(self):
        if not os.system('ping 8.8.8.8'):
            self.connected=True
        else:
            self.connected=False
