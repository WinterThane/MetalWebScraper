from bs4 import BeautifulSoup
from lxml import html
import urllib

url = urllib.request.urlopen('https://www.metal-archives.com/browse/letter')
content = url.read()
soup = BeautifulSoup(content, "html.parser")

tmp = soup.find_all('a')
lettersList = tmp[23:]

with open('BandLetters.txt', 'w') as outfile:   
    for link in lettersList:
        outfile.write('%s\n' % link.get('href'))