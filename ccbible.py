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
import re
from urlsearch import *

gDebug = True    # True
  
class CCBibleStudy(CommonUrlSearch):
  '''
  
  http://www.ccbiblestudy.org/Old%20Testament/02Exo/02index-T.htm
  '''
  def __init__(self, url="", enc=""):
    #url = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/05.htm"
    super().__init__(url)
    self.myInit()

  def myInit(self):
    self._ccblBooks = {}

  def collectContent(self):
    keys = self._ccblBooks.keys()
    testBreak = True
    print("collecting...%d books" % (len(keys)))
    for key in keys:
      url   = self._ntmFFchapters[key]
      fname = "/storage/emulated/0/Documents/CCBL_" + key + ".txt"
      fd = open(fname,"w")
      # regeneration of soup tree
      self.myinit(url, "big5", True)
      self.printSoupBodyByItem(fd)
      print("...,,,"*7)
      print("\n")
      '''
      if testBreak: # break out of the loop for testing
        print("fname = %s" % (fname))
        break
      '''

  def collectIndexPageInfo(self, url, enc = "", forcedZip = False):
    self._url = url
    req = request.Request(url, None, self._headers)
    req.add_header('Accept-encoding', 'gzip')
    response = request.urlopen(req)
    htmlIndex = response.read()
    gzipped = response.headers.get('Accept-Encoding') #'Content-Encoding')

    print("gzipped::", gzipped)
    if gzipped or forcedZip:
      htmlIndex = zlib.decompress(htmlIndex, 16+zlib.MAX_WBITS)
    ###print(html)
    if enc == "":
      print("### utf-8 ###")
      self._htmlIndex = htmlIndex.decode("utf-8", "ignore")
    else:
      print("### enc ###")
      self._htmlIndex = htmlIndex.decode(enc, "ignore")
      
    
        
    print("@@@ collectIndexPageInfo @@@ %s" % (url))
    print(self._htmlIndex)
    self._soupIndex = BeautifulSoup(self._html, "html.parser")
  
  def printSep(self, symb= "-"):
    print(symb*35)
    
  def getNextEntry(self, strSrc, strPtn = ""):
    ptnStart = "<a"
    ptnEnd   = "</a>"
    strTemp  = strSrc
    strRes   = strSrc
    
    indxStart = strTemp.find(ptnStart)
    indxEnd   = strTemp.find(ptnEnd)
    
    indxNext  = indxEnd+len(ptnEnd)
    strTgt    = strTemp[indxStart:indxNext]
    strTemp   = strTemp[indxNext:]
    strChk    = strTemp[indxNext:indxNext+10]
    print("nextEntry:%s nextEntry:%s" % (strTgt, strChk))
    
    return strTgt, strTemp
    
    
    
    
  
  def collectBookLinks(self):
    dctLinks = {}
    strTemp = str(self._htmlIndex)
    #strTgt  = self.removeAllTags(strTemp)
    
    # self._ccblBooks
    # collect <a ... </a>
    numTgtLinks = strTemp.count("<a")
    print("numLinks = %d" % (numTgtLinks))
    strRes = strTemp
    j = 0
    ptnInclude = "Testament"
    for i in range(numTgtLinks):
      strEntry, strRes = self.getNextEntry(strRes)
      if strEntry.find(ptnInclude) != -1:  # found
        dctLinks[j] = strEntry
        j += 1
    
    for key in dctLinks.keys():
      print("dLonks[%d]::%s" % (key, dctLinks[key]))
    
  def removeAllTags(self, strSrc):
    # remove <…> 
    # s[start:end+1] = "<…>"
    tagStart  = '<'
    tagEnd    = '>'
    strTemp   = str(strSrc)
    indxStart = -1
    indxEnd   = -1
    cntLoop   = 1
    strTemp   = strTemp.replace("<p>",  "\n")
    strTemp   = strTemp.replace("</p>", "\n")
    
    print("SSS:::%s" % (strTemp))
    #input("A0:Enter any key to proceed")
    lpCondition = True
    while lpCondition:
      lnStrTemp = len(strTemp)
      indxStart = strTemp.find(tagStart)
      self.printSep()
      print(">>>--%s\n" % (strTemp))
      if indxStart != -1:  # found
        indxEnd = strTemp.find(tagEnd)
        print("222:: indxStart[%d] indxEnd[%d]" % (indxStart, indxEnd))
        
        '''
        indxOne = indxStart -5
        if indxOne < 0:
          indxOne = 0
        indxTwo = indxStart +5
        neighbor1 = strTemp[indxOne:indxTwo]
        
        indxOne = indxEnd -5
        indxTwo = indxEnd +5        
        neighbor2 = strTemp[indxOne:indxTwo]        
        print("B01 --%s-- vs --%s--" % (neighbor1, neighbor2))
        '''
        
        if indxEnd != -1:  # found
          indxEnd = indxEnd+1
          strTgt  = strTemp[indxStart:indxEnd]
          #strTgt  = strTemp[indxStart:indxStart*2]
          strTgt1 = strTgt[1:]
          print("333:: @@@ @@@strTgt[%s], strTgt1[%s]" % (strTgt, strTgt1))
          '''
          <a href="Old%20Testament/33Micah/33index-T.htm">
            33
            <span lang=EN-US>
             <span lang=EN-US>
               彌迦書
             </span>
            </span>
          </a>
             
          <a href="Old%20Testament/34Nah/34index-T.htm">
            34
            <span lang=EN-US>
              <span lang=EN-US>
                那鴻書
              </span>
            </span>
          </a>
                      
          '''
          
          if strTgt1.find(tagStart) != -1:   # found <…<…> do nothing
            print("<…<…> Error::%s" % (strTgt))
            lpCondition = False
          else:
            print("REM:: remove:%s" % (strTemp[indxStart:indxEnd]))
            strFront = strTemp[:indxStart]
            strBack  = strTemp[indxEnd:]
            strTemp  = strFront + strBack
            print("RES:: %s" % (strTemp))
            self.printSep()
          cntLoop += 1
          #input("Enter any key to proceed")
        else:  # tagEnd isnot found -> "<…"
          pront(";;;")
          lpCondition = False
      else:
        lpCondition = False
      
    return strTemp



def main():
  url = "http://www.ccbiblestudy.org/index-T.htm"
  enc = "big5"
  forceDecomp = True
  ccBS = CCBibleStudy(url, enc)
  ccBS.printSep()
  ccBS.collectIndexPageInfo(url, enc, forceDecomp)
  ccBS.printSep("=")
  ccBS.collectBookLinks()

if __name__ == "__main__":
  main()

