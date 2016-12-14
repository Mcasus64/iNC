# -*- coding: utf-8 -*-
import urllib
import urllib.request as request
import urllib.parse as parse
import re 
from bs4 import BeautifulSoup 
from datetime import datetime 
import gzip
import io
import zlib
import unicodedata
import time
from urlsearch import *

# 荷蘭華人基督教會
'''
url = "http://www.ccgn.nl/boeken02_e.html"

self.dctCCGN[“暗室之後“］   = "http://www.ccgn.nl/boekeseln02/aszh/knjy14.htm"
self.dctCCGN[“暗室之後續“］ = "http://www.ccgn.nl/boeken02/aszh/xj/knjy15.htm"

'''


class DrTongSBLS(CommonUrlSearch):
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    self.myInit(url, "big5", True)
    self.dct = {}


  def myInit(self, url, enc = "", forcedZip = False):
    print("myInit()::url = %s", (url))
    self.myinit(url, enc, forcedZip)
    
  def getOne(self, url):
    self.myInit(url, "big5", True)
    strRes = self.collectBody()
    return strRes
    
  def collectBatch(self, iStart, iEnd, uBase, uExt, fBase, fExt):
    '''
    '''
    for item in range(iStart, iEnd):
      strI = str(item)
      url  = uBase + strI + uExt
      
      strRes = self.getOne(url)
      ###print(strI * 25)
      ###print(strTgt)
      fname = fBase + strI + fExt
      
      if strRes == "":
        print("item[%s]:: url error - content empty" % (item))
      else:
        fd = open(fname,"w")
        fd.write(strRes)
        self.printSep("#")
        print("file:%s collected." % (fname))
        fd.close()
      fname = ""

  def collectListBatch(self, lstUrls, uBase, uExt, fBase, fExt):
    '''
    '''
    for item in lstUrls:
      strI = str(item)
      url  = uBase + strI + uExt
      
      strRes = self.getOne(url)
      ###print(strI * 25)
      ###print(strTgt)
      fname = fBase + strI + fExt
      
      if strRes == "":
        print("item[%s]:: url error - content empty" % (item))
      else:
        fd = open(fname,"w")
        fd.write(strRes)
        self.printSep("#")
        print("file:%s collected." % (fname))
        fd.close()
      fname = ""

  def collectSermons(self):
    '''
    1-23, 26-43
    exceptions: 
    24a, 24b, 24c
    25a, 25b, 25c
    '''
    urlBase = "http://www.ccgn.nl/boeken02/xbls/"
    urlExt  = ".htm"
    fExt    = ".txt"
    fBase   = "/storage/emulated/0/Documents/xbls_" 
    numLectures = 43+1
    
    ###self.collectBatch(iStart, iEnd, uBase, uExt, fBase, fExt)
    ###self.collectBatch(1, 24, urlBase, urlExt, fBase, fExt)
    
    # self.collectListBatch(self, lstUrls, uBase, uExt, fBase, fExt)
    # get 24a, 24b, 24c, 25a, 25b, and 25c
    lstUrls = ["24a", "24b", "24c", "25a", "25b", "25c"]
    ###self.collectListBatch(lstUrls, urlBase, urlExt, fBase, fExt)
    
    self.collectBatch(26, 44, urlBase, urlExt, fBase, fExt)
    
    
    
def main():
  url = "http://www.ccgn.nl/boeken02/xbls/1.htm"
  sblsScraper = DrTongSBLS(url)
  
  sblsScraper.collectSermons()
  
if __name__ == "__main__":
  main()

