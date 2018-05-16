from bs4 import BeautifulSoup
import urllib
import json

url = urllib.request.urlopen('https://www.metal-archives.com/browse/ajax-letter/l/Z/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart=0')
tmp = ""
recNumber = 0
x = []

def GetRecNumberLine():
    counter = 0
    global tmp
    for line in url:
        if counter == 1:
            tmp = line
            break
        counter += 1

def GetRecNumber():
    global recNumber
    for d in tmp.split():
        d = d.decode("utf-8").replace(",", "")
        if d.isdigit():
            recNumber = d

GetRecNumberLine()
GetRecNumber()

print(recNumber)
