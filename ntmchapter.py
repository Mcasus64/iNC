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
  
class NTMFirmFoundation(CommonUrlSearch):
  '''
  
  '''
  def __init__(self, url="", enc=""):
    #url = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/05.htm"
    super().__init__(url)
    self.myInit()
        ## remove and replace of extra tags
    # remove </a>
    self._dctReplaceTags = {}
    self._dctReplaceTags["</a>"]   = " "
    # replace <p> </p> with "\n"
    self._dctReplaceTags["<p>"]    = "\n"
    self._dctReplaceTags["</p>"]   = "\n"
    self._dctReplaceTags["<pre>"]  = "\n"
    self._dctReplaceTags["</pre>"] = "\n\n"
    self._dctReplaceTags["<br/>"]  = "\n"

    
  def myInit(self):
    self._ntmFFchapters = {}
    self._ntmFFchapters["00"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/30.htm"
    self._ntmFFchapters["01"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/01.htm"
    self._ntmFFchapters["02"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/02.htm"
    self._ntmFFchapters["03"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/03.htm"
    self._ntmFFchapters["04"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/04.htm"
    self._ntmFFchapters["05"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/05.htm"
    self._ntmFFchapters["06"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/06.htm"
    self._ntmFFchapters["07"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/07.htm"
    self._ntmFFchapters["08"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/08.htm"
    self._ntmFFchapters["09"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/09.htm"
    self._ntmFFchapters["10"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/10.htm"
    self._ntmFFchapters["11"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/11.htm"
    self._ntmFFchapters["12"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/12.htm"
    self._ntmFFchapters["13"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/13.htm"
    self._ntmFFchapters["14"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/14.htm"
    self._ntmFFchapters["15"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/15.htm"
    self._ntmFFchapters["16"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/16.htm"
    self._ntmFFchapters["17"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/17.htm"
    self._ntmFFchapters["18"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/18.htm"
    self._ntmFFchapters["19"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/19.htm"
    self._ntmFFchapters["20"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/20.htm"
    self._ntmFFchapters["21"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/21.htm"
    self._ntmFFchapters["22"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/22.htm"
    self._ntmFFchapters["23"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/23.htm"
    self._ntmFFchapters["24"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/24.htm"
    self._ntmFFchapters["25"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/25.htm"
    self._ntmFFchapters["26"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/26.htm"
    self._ntmFFchapters["27"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/27.htm"
    self._ntmFFchapters["28"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/28.htm"
    self._ntmFFchapters["29"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/29.htm"
    self._ntmFFchapters["30"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/30.htm"
    self._ntmFFchapters["31"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/31.htm"
    self._ntmFFchapters["32"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/32.htm"
    self._ntmFFchapters["33"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/33.htm"
    self._ntmFFchapters["34"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/34.htm"
    self._ntmFFchapters["35"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/35.htm"
    self._ntmFFchapters["36"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/36.htm"
    self._ntmFFchapters["37"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/37.htm"
    self._ntmFFchapters["38"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/38.htm"
    self._ntmFFchapters["39"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/39.htm"
    self._ntmFFchapters["40"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/40.htm"
    self._ntmFFchapters["41"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/41.htm"
    self._ntmFFchapters["42"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/42.htm"
    self._ntmFFchapters["43"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/43.htm"
    self._ntmFFchapters["44"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/44.htm"
    self._ntmFFchapters["45"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/45.htm"
    self._ntmFFchapters["46"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/46.htm"
    self._ntmFFchapters["47"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/47.htm"
    self._ntmFFchapters["48"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/48.htm"
    self._ntmFFchapters["49"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/49.htm"
    self._ntmFFchapters["50"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/50.htm"
    self._ntmFFchapters["51"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/51.htm"
    self._ntmFFchapters["52"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/52.htm"
    self._ntmFFchapters["53"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/NTM_FirmFoundations/b5/53.htm"
    self._ntmFFchapters["54"] = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/54.htm"
    #                                   www.jidujiao.com/zhuanti/xinyangbaoku

  def collectContent(self):
    keys = self._ntmFFchapters.keys()
    testBreak = True
    print("collecting...%d chapters" % (len(keys)))
    for key in keys:
      url   = self._ntmFFchapters[key]
      fname = "/storage/emulated/0/Documents/NTM_" + key + ".txt"
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

  def removeTags(self, strTgt, strTag, strRep):
    strTemp = strTgt
    strTemp = strTemp.replace(strTag, strRep)
    
    return strTemp


  def removeLinks(self, strSrc):
    ptnTa   = "<a"
    ptnTail = ">"
    ptnT_a  = "</a>"
    strTgt = strSrc
    ###print("removeLinks : %s" % (strTgt))
    
    cntTa = strTgt.count(ptnTa)
    print("Tag a count :%d" % (cntTa))
    #obj = self._dctReplaceTags
    
    for i in range( cntTa ):
      indxPtnTa   = strTgt.find(ptnTa)
      strFront    = strTgt[: indxPtnTa]
      strTemp     = strTgt[ indxPtnTa :]
      indxPtnTail = strTemp.find( ptnTail )
      indxPtnTail = indxPtnTa + indxPtnTail
      strBack     = strTgt[ indxPtnTail+1 :]
      strRem      = strTgt[ indxPtnTa: indxPtnTail+1]
      
      print("indexes@@%d::%d  " % ( indxPtnTa, indxPtnTail ))
      print("Str = %s" % ( strRem ))
      
      strTgt = strFront + strBack
      
      # replace tags
      keys = self._dctReplaceTags.keys()
      for key in keys:
        strTag = key
        strRep = self._dctReplaceTags[key]
        strTgt = self.removeTags(strTgt, strTag, strRep)
      
    return strTgt
    
    
  def printSoupBodyByItem(self, fd = ""):
    body = self.getSoup().body
    if body != None :
      indxBdy = 1
      if fd != "":
        for item in body:
          #fd.write("÷÷÷"*12)
          strItem = item
          strSep = "---"*8
          print("%d::%s" % (indxBdy, strSep))          #strItem = self.removeLinks( strItem )
          strItem = self.removeAllTags(strItem)
          strSep = "###"*8
         
          fd.write(strItem)
          indxBdy += 1
        fd.close()
      else:     
        for item in body:
          print("÷÷÷"*12)
          print("\n@@@%d == %s" % (indxBdy, item))
          indxBdy += 1
      
      print("numBdyItems = %d" % (indxBdy))
    

def main():
  #url = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/05.htm"
  url = "http://www.cheeridea.asia/su101/2016-12-1/mobile/index.html#p=15"
  enc = "big5"
  ntmScraper = NTMFirmFoundation(url, enc)
  ntmScraper.collectContent()
  ###strTst = '<html xmlns="http://www.w3.org/TR/REC-html40"><head><meta http-equiv=Content-Type content="text/html; charset=big5"><title>穩固根基 第二十七課 以色列的不信神的1/4f判及拯救</title><style>'
  ###strRes = ntmScraper.removeAllTags(strTst)
  ###print("@@@@@@@:::%s\n" % (strRes))


if __name__ == "__main__":
  main()