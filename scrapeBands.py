from bs4 import BeautifulSoup
import urllib
import json

urlPrefix = "https://www.metal-archives.com/browse/ajax-letter/l/"
urlLetter = "Z"
urlSuffix = "/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart=0"

url = urllib.request.urlopen(urlPrefix + urlLetter + urlSuffix)

def GetRecNumberLine(url):
    counter = 0
    for line in url:
        if counter == 1:
            return line
        counter += 1

tmp = GetRecNumberLine(url)

def GetRecNumber(line):
    for d in line.split():
        d = d.decode("utf-8").replace(",", "")
        if d.isdigit():
            return d

recNumber = GetRecNumber(tmp)

print(recNumber)
