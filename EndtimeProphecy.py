from urlsearch import *
import io, zipfile, sys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary 


gDebug = True

class EndTimeUrl(CommonUrlSearch):
  '''
  refer to wwwDsigns-of-end-timesDcomSaboutDhtml-WhatWeBelieve.txt
  '''
  def __init__(self, url):
    super().__init__(url)
    self.lstSoupAllParagraphs = self._soup.find_all("p")
    self.lstSoupAllLinks = self._soup.find_all("a")
    
  def getAllParagraphs(self, format = False):
    indxCnt = 1
    if format:
      for paragraph in self.lstSoupAllParagraphs:        
        print("==="*8)
        print("%d::" % (indxCnt), paragraph)
        indxCnt+= 1
    else: # not to format
      print(self.lstSoupAllParagraphs)
      
    print("num list entries:: %d" % (len(self.lstSoupAllParagraphs)))


  def getAllParagraphText(self, output2File = False):
    if output2File:
      #fBase = "/storage/0123-4567/church/endtime/"
      fBase = "/storage/emulated/0/Documents/"
      fn = fBase + self.html2Str(self._url) + ".txt"
      fd = open(fn, "w")
      
    sep = "=="*8
    indxCnt = 1
    for paragraph in self.lstSoupAllParagraphs:
      #strResult = self.cleansePunct(paragraph.text)
      strResult = self.cleanseFormat(paragraph.text)
      entry = "%d::%s" % (indxCnt, strResult)
      if strResult.isspace() == False:
        print(sep)
        print(entry)
        indxCnt += 1
        if output2File:
          fd.write(sep+"\n")
          fd.write(entry+"\n")
    numEntries = ("self._url:: %s" % (self._url))
    print(numEntries)
    if output2File:
      fd.write(sep+"\n")
      fd.close()
      
  def getText(self, option = ""):
    print("-------getText-------")
    '''
    if option == "p":
      for itemP in self._soup.p:
        print("s.get_text()::%s" % (itemP.get_text()))
    '''
    lstPs = self._soup.find_all("p")
    cnt = 1
    sep = ("---"*9)
    print("lenLstPs ::%d" % (len(lstPs)))
    for p in lstPs:
      print("pText: \n%d\n::%s\n" %  (cnt, p.get_text()))
      cnt +=1
  
  
  
      
class SignsOfEndTimesDotCom(EndTimeUrl):
  def __init__(self, url):
    super().__init__(url)

    
class NthuEndTimeProphecy(EndTimeUrl):
  def __init__(self, url):
    super().__init__(url)


class GotQuestionOnEndTimeProphecy(EndTimeUrl):
  '''
  request = urllib2.Request(url)

request.add_header('Accept-encoding', 'gzip')

opener = urllib2.build_opener()

response = opener.open(request)html = response.read()

gzipped = response.headers.get('Content-Encoding')

if gzipped:

    html = zlib.decompress(html, 16+zlib.MAX_WBITS)

print html

  '''
  def __init__(self, url):
    super().__init__(url)


  
   
class ZippedUrlNews():
  def __init__(self, url):
    self._headers = {#'Accept':'text/css,*/*;q=0.1', 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
    'Accept-Encoding':'gzip,deflate,sdch', 
    'Accept-Language':'en-US,en;q=0.8', 
    #'User-Agent':'Mozilla/5 (Solaris 10) Gecko'} 
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}

    
    self.myinit(url)
    
    # html codes
    self._ptnHtmlCode = '&#[0-9]+[;]'
    self._reHtmlCode  = re.compile(self._ptnHtmlCode)
    self._ptnPunct    = '[><}{)(.,"]+'
    self._rePunct     = re.compile(self._ptnPunct)
    self._ptnFormat   = '&[a-zA-Z;]+'
    self._reFormat    = re.compile(self._ptnFormat)

  def myinit(self, url):
    self._url = url
    
    req = request.Request(url, None, self._headers)
    response = request.urlopen(req)
    data = gzip.decompress(response.read()) 
    data = str(data,'utf-8')
    
    print(data)
    print("@@@"*20)
    
    self._soup = BeautifulSoup(data, "html.parser")
    self.lstSoupAllParagraphs = self._soup.find_all("p")
    self.lstSoupAllLinks = self._soup.find_all("a")

  def printInfo(self, printLink = False):
    ###print(self._soup.prettify())
    result = self._soup.find_all('p') 
    
    print("printing...")
    print("#lenResult: ", len(result))
    if printLink == True:
      for elem in result: 
         print(elem)###.encode("utf-8")) this causes hex string to be pronted!!!

        # for i in final_list: 
        #   print (i)
        # print (final_list)
    else:
      print(self._soup.prettify())

  def cleanseAll(self, strSrc):
    strSrc = self._reHtmlCode.sub("", strSrc)
    strSrc = self._rePunct.sub("", strSrc)
    strSrc = self._reFormat.sub("", strSrc)
    return strSrc
    
  def cleanseHtmlCode(self, strSrc):
    strSrc = self._reHtmlCode.sub("", strSrc)
    return strSrc

  def cleansePunct(self, strSrc):
    strSrc = self._rePunct.sub("", strSrc)
    return strSrc

  def cleanseFormat(self, strSrc):
    strSrc = self._reFormat.sub("", strSrc)
    return strSrc

  

  def html2Str(self, strHtml):
    self._dctHtml2Str = {
    	"." : "DOT",
    	"/" : "SLA",
    	":" : "SEM",
    	"," : "COM"
    	}
    	
    '''
    Convert typical HTML address to str
    www.abc-def.com/index.html
    to
    wwwDOTabc-defDOTcomSLAindexDOThtml
    '''
    strTarget = strHtml
    keys = self._dctHtml2Str.keys()
    for key in keys:
      val = self._dctHtml2Str.get(key)
      strTarget = strTarget.replace(key, val)
    print("---"*8)
    print("strTarget::%s " % (strTarget))
    return strTarget
    

  def str2Html(self, strSrc):
    '''
    Revert typical HTML converted str to address
    wwwDOTabc-defDOTcomSLAindexDOThtml
    to
    www.abc-def.com/index.html
    
    '''
    strTarget = strSrc
    vals = self._dctHtml2Str.values()
    keys = self._dctHtml2Str.keys()
    for val in vals:
      for key in keys:
        valk = self._dctHtml2Str.get(key)
        if val == valk:
          strTarget = strTarget.replace(val, key)
    
    print("---"*8)
    print("strTarget::%s " % (strTarget))
    return strTarget
    
  def getAllParagraphText(self, output2File = False):
    if output2File:
      #fBase = "/storage/0123-4567/church/endtime/"
      fBase = "/storage/emulated/0/Documents/"
      fn = fBase + self.html2Str(self._url) + ".txt"
      fd = open(fn, "w")
    
    indxCnt = 1
    print("len::%d" % (len(self.lstSoupAllParagraphs)))
    for paragraph in self.lstSoupAllParagraphs:
      sep = "=="*8
      #strResult = self.cleansePunct(paragraph.text)
      strResult = self.cleanseFormat(paragraph.text)
      entry = "%d::%s" % (indxCnt, strResult)
      if strResult.isspace() == False:
        print(sep)
        print(entry)
        indxCnt += 1
        if output2File:
          fd.write(sep+"\n")
          fd.write(entry+"\n")
    numEntries = ("self._url:: %s" % (self._url))
    print(numEntries)
    if output2File:
      fd.write(sep+"\n")
      fd.close()
    
  def getAllLinks(self, output2File = False, optLnkText = False):
    print("-------getAllLinks-------")
    cnt = 1
    for link in self.lstSoupAllLinks:
      print("---"*9)
      if optLnkText == False:
        print("lText[%d]::\n%s"%(cnt, link))
      else:   # True get text part of <a>
        lText = link.get_text(strip=True)
        lText = str(lText)
        if lText.isspace() == False:
          ###if lText != "":
          ###if lText.isspace() == False:
            print("lText[%d]::\n>>%s<<" % (cnt, lText))
        else:
          print("lText[%d]:: empty" % (cnt))

      cnt += 1
    print("numLnks::%d"%(len(self.lstSoupAllLinks)))


class YNetNews(ZippedUrlNews):
  def __init__(self, url):
    # http://www.ynetnews.com/home/0,7340,L-3083,00.html
    super().__init__(url)
      
class HaaretzNews(ZippedUrlNews):
  def __init__(self, url):
    # http://www.haaretz.com/?v=
    super().__init__(url)
    
class JpostDcom(ZippedUrlNews):
  def __init__(self, url):
    # http://www.jpost.com
    super().__init__(url)
    
class TimesOfIsrael(ZippedUrlNews):
  def __init__(self, url):
    # http://www.timesofisrael.com
    super().__init__(url)
  
  def getNewsTitles(self):
    print("-------getNewsTitles-------")
    #soup.find(string=re.compile("sisters"))
    titles = self._soup.find(string=re.compile("title"))
    cnt = 0
    
    #cnt = len(titles)
    print("found %d titles" % (cnt))
    print("attrs of s.a :;" % self._soup.a.attrs)
  
  
  
  

#######
def ynetNews():
  strUrl = "http://www.ynetnews.com/home/0,7340,L-3083,00.html"
  ynetNews = YNetNews(strUrl)
  ynetNews.getAllLinks()

def haaretzNews():
  strUrl = "http://www.haaretz.com/?v="
  haaretz = HaaretzNews(strUrl)
  #haaretz.getAllParagraphText()
  #haaretz.getText("p")
  haaretz.getAllLinks(False, True)
  
def jpostDcom():
  strUrl = "http://www.jpost.com/"
  jpost = JpostDcom(strUrl)
  jpost.getAllLinks(False, True)

def timesIsrael():
  strUrl = "http://www.timesofisrael.com"
  tIsrael = TimesOfIsrael(strUrl)
  tIsrael.getAllLinks(False, True)
  tIsrael.getNewsTitles()

def gotQuestions():
  strUrl = "https://www.gotquestions.org/T-Chinese/T-Chinese-end-times.html"
  gotQuestions = GotQuestionOnEndTimeProphecy(strUrl)
  gotQuestions.getAllParagraphText()   # decode("big5", "ignore")
  
  
  
def nthuEndtimeProphecy():
  strUrl = "http://ling.nthu.edu.tw/faculty/thlin/faith/endtime_prophecy.htm"
  nthuEndTimeProphecy = NthuEndTimeProphecy(strUrl)
  nthuEndTimeProphecy.getAllParagraphText()   ### True)



def searchSignsOfEndTimesDotCom():
  strUrl = "http://www.signs-of-end-times.com"
  
  signsOfEndTimes = SignsOfEndTimesDotCom(strUrl)
  
  ###signsOfEndTimes.printInfo()
  ###signsOfEndTimes.getAllParagraphs(True)
  ###signsOfEndTimes.getAllParagraphText()
  ###strHtml = signsOfEndTimes.html2Str(strUrl)
  ###signsOfEndTimes.str2Html(strHtml)
  signsOfEndTimes.getAllParagraphText(True)
  signsOfEndTimes.getText("p")
  
class IsraelHayom():
  def __init__(self, url):
    self.url = url
    
  def useSelenium(self):
    binary = FirefoxBinary('/data/data/com.hipipal.qpy3/files/lib/python3.2/site-packages') 

    browser = webdriver.Firefox(firefox_binary=binary)
    browser.get(self.url)
    sleep(10)
    body = browser.find_element_by_id('body')
    print(body)
    
    
    
  def useMechanize(self):
    mb = mechanize.Browser()
    mb.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1.fc9 Firefox/3.0.1')]
    mb.set_handle_robots(False)
    response =mb.open(self.url).read()
    print(response)
  
  
def iHayom():
  strUrl = "http://www.israelhayom.com/site/today.php"

  ihayom = IsraelHayom(strUrl)
  #ihayom.getAllParagraphText(True)
  #ihayom.getText("p")
  ihayom.useSelenium()
  #ihayom.useMechanize()

  

def main():
  ###searchSignsOfEndTimesDotCom()
  #nthuEndtimeProphecy()
  #gotQuestions()
  ###ynetNews()
  ###searchSignsOfEndTimesDotCom()
  ###haaretzNews()
  ###jpostDcom()
  #timesIsrael()
  iHayom()
  
  

if __name__ == "__main__":
  main()

