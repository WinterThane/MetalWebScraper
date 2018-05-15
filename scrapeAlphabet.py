from bs4 import BeautifulSoup
import urllib
import json

url = urllib.request.urlopen('https://www.metal-archives.com/browse/letter')
soup = BeautifulSoup(url.read(), "html.parser")

tmp = soup.find_all('a')
lettersList = tmp[23:]

result = []

def CleanList():
    for link in lettersList:
        result.append(link.get('href'))

with open('BandLetters.txt', 'w') as outfile:   
    CleanList()
    json.dump(result, outfile, indent=1)