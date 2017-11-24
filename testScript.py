import os
import sys
import getpass
from bible import bible


bibleKJV=bible()
bibleKJV.load('KJV',True)

bibleNKJV=bible()
bibleNKJV.load('NKJV',True)



bibleGNV=bible()
bibleGNV.load('GNV',True)


bibleHCSB=bible()
bibleHCSB.load('HCSB',True)

