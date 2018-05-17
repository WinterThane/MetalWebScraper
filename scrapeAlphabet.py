from bs4 import BeautifulSoup
import urllib


url = urllib.request.urlopen('https://www.metal-archives.com/browse/letter')
soup = BeautifulSoup(url.read(), "html.parser")


tmp = soup.find_all('a')
lettersList = tmp[23:]
output = []


def extract_link():   
    for link in lettersList:
        output.append(link.get('href'))


def extract_letters():
    extract_link()
    tmp = []
    for line in output:
        x = line.split("/")
        tmp.append(x[-1])
    return tmp


def write_file():
    with open('Alphabet.txt', 'w') as outfile:   
        extract_link()
        for link in output:
            outfile.write('%s\n' % link)


if __name__ == "__main__":
    write_file()