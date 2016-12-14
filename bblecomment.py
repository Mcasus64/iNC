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


class BbleCommentaryScraper(CommonUrlSearch):
  '''
  '''
  def __init__(self, url, enc = ""):
    super().__init__(url, enc)
    #self.myInit()
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
    
    '''
    fhl commentary
    '''
    self.myInit()
      
  def myInit(self):
    self._bblBooks = {}
    print("hello world")
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Gen"]   = "01創世記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Ex"]    = "02出埃及記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Lev"]   = "03利未記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Num"]   = "04民數記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Deut"]  = "05申命記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Josh"]  = "06約書亞記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Judg"]  = "07士師記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Ruth"]  = "08路得記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=1+Sam"] = "09撒母耳記上"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=2+Sam"] = "10撒母耳記下"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=1+Kin"] = "11列王紀上"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=2+Kin"] = "12列王紀下"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Ezra"]  = "15以斯拉記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Neh"]   = "16尼希米記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Esth"]  = "17以斯帖記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Job"]   = "18約伯記"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Prov"]  = "20箴言"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Eccl"]  = "21傳道書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Song"]  = "22雅歌"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Is"]    = "23以賽亞書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Jer"]   = "24耶利米書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Lam"]   = "25耶利米哀歌"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Ezek"]  = "26以西結書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Dan"]   = "27但以理書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Hos"]   = "28何西阿書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Joel"]  = "29約珥書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Amos"]  = "30阿摩司書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Obad"]  = "31俄巴底亞書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Jon"]   = "32約拿書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Mic"]   = "33彌迦書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Nah"]   = "34那鴻書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Hab"]   = "35哈巴谷書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Zeph"]  = "36西番雅書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Hag"]   = "37哈該書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Zech"]  = "38撒迦利亞書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Mal"]   = "39瑪拉基書"

    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Matt"]  = "40馬太福音"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Mark"]  = "41馬可福音"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Luke"]  = "42路加福音"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=John"]  = "43約翰福音"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Acts"]  = "44使徒行傳"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Rom"]   = "45羅馬書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=1+Cor"] = "46哥林多前書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=2+Cor"] = "47哥林多後書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Gal"]   = "48加拉太書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Eph"]   = "49以弗所書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Phil"]  = "50腓立比書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Col"]   = "51歌羅西書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=1+Thess"]  = "52帖撒羅尼迦前書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=2+Thess"]  = "53帖撒羅尼迦後書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=1+Tim"]    = "54提摩太前書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=2+Tim"]    = "55提摩太後書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Titus"]    = "56提多書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Philem"]   = "57腓利門書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Heb"]      = "58希伯來書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=James"]    = "59雅各書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=1+Pet"]    = "60彼得前書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=2+Pet"]    = "61彼得後書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=1+John"]   = "62約翰一書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=2+John"]   = "63約翰二書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=3+John"]   = "64約翰三書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Jude"]     = "65猶大書"
    self._bblBooks[ "http://a2z.fhl.net/php/pcom.php?book=3&engs=Rev"]      = "66啟示錄"
    
    
  def printSoupInfo(self):
    numPre = len(self.getSoup().pre)
    numP   = len(self.getSoup().p)
    strHtml = self._html
    ptnVerse = "經文："
    ptnComment = "註釋:"
    cntVerse = strHtml.count(ptnVerse)
    cntComment = strHtml.count(ptnComment)
    lenSoupContents = len(self.getSoup().contents)
    
    print("Bsoup, info. \n --------------")
    print("numPre      = %d" % (numPre))
    print("numP        = %d" % (numP))
    print("cntVerse    = %d" % ( cntVerse ))
    print("cntComment  = %d" % ( cntComment ))
    print("lenContents = %d" % ( lenSoupContents ))


def main():
  '''
  #fBase = "/storage/0123-4567/church/endtime/"
  fBase = "/storage/emulated/0/Documents/"  
  '''
  fBase = "/storage/emulated/0/Documents/"  
  fName = fBase + "fhlTemp.txt"
  fd = open(fName, "w")
  
  '''
  01:Genesis
  http://a2z.fhl.net/php/pcom.php?book=3&engs=Gen
  02:Exodus
  http://a2z.fhl.net/php/pcom.php?book=3&engs=Ex
  
  各卷註釋
  <table width=70%  border=1>
  <tr>
  </tr>
  </table>
  '''
  
  #url = "http://a2z.fhl.net/php/pcom.php?book=3&engs=Jer"
  url = "http://www.jidujiao.com/zhuanti/xinyangbaoku/Books/NTM_FirmFoundations/b5/05.htm"
  
  bblScraper = BbleCommentaryScraper(url, "big5")
  ###bblScraper.printInfo() 
  ###bblScraper.printSoupInfo()
  ###bblScraper.printSoupBodyByItem(fd)
  ###bblScraper. scraperCollect()
  
  
if __name__ == "__main__":
  main()
