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



class WIKIScraper(CommonUrlSearch):
  '''
  
  '''
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    self.myInit(url, "", True)
    self.dct = {}


  def myInit(self, url, enc = "", forcedZip = False):
    print("myInit()::url = %s", (url))
    self.myinit(url, enc, forcedZip)

  def getOne(self, url, upperTags = False, forceZip = True):
    strTgt = ""
    try:
      self.myInit(url, "", forceZip)
      strTgt  = self.collectBody(upperTags, forceZip)
    except urllib.error.HTTPError as err:
      print("urllib.error.HTTPError::", err)
   
    return strTgt
    
  def collectBody(self, upperTags = False, stripTags = True):
    if upperTags:
      body = self.getSoup().BODY
    else:
      body = self.getSoup().body
    self.printSep("€")
    strBody = str(body)
    if upperTags:
      strBody = strBody.replace("<BR>","\n")
    else:
      strBody = strBody.replace("<br>","\n")
    if stripTags:
      strBody = self.removeAllTags(strBody)
    ###print(strBody)
    return strBody



def main():
  url = "https://en.m.wikipedia.org/wiki/Christian_eschatology"


  wikiScraper = WIKIScraper(url)
  strTgt = wikiScraper.getOne(url)
  wikiScraper.printSep("@")
  print(strTgt)
  ###print("Result: %s" %(wikiScraper.getSoup().text))


if __name__ == "__main__":
  main()
