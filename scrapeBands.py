import urllib, urllib.request, json
from html.parser import HTMLParser
from bs4 import BeautifulSoup

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


urlPrefix = "https://www.metal-archives.com/browse/ajax-letter/l/"
urlLetter = "Z"
urlSuffix = "/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart="
outputFile = urlLetter + "_Bands.txt"
url = urllib.request.urlopen(urlPrefix + urlLetter + urlSuffix + "0")


def get_rec_number_line(lines):
    counter = 0
    for line in lines:
        if counter == 1:
            return line
        counter += 1


def get_rec_number(line):
    for d in line.split():
        d = d.decode("utf-8").replace(",", "")
        if d.isdigit():
            return d


tmp = get_rec_number_line(url)
result = []
output = []


def get_records():
    recNumber = int(get_rec_number(tmp))
    counter = 0
    while counter < recNumber:
        with urllib.request.urlopen(urlPrefix + urlLetter + urlSuffix + str(counter)) as url:
            data = json.loads(url.read().decode())
            result.append(data['aaData'])
            counter += 500


def fix_band_name(xx):
    x = BeautifulSoup(xx, "html.parser")
    name = x.get_text()  
    for link in x.find_all('a'):
        lnk = link.get('href')       
    return name, lnk


def make_new_json():
    get_records()   
    for lines in result:   
        for line in lines:
            nameLink = fix_band_name(line[0])
            newJson = {}
            newJson["Name"] = nameLink[0]
            newJson["Link"] = nameLink[1]
            newJson["Country"] = line[1]
            newJson["Genre"] = line[2]
            newJson["Status"] = strip_tags(line[3])
            output.append(newJson)            
    json.dumps(output, ensure_ascii=False)


def write_to_file():
    make_new_json()
    with open(outputFile, 'w') as outfile:   
        json.dump(output, outfile, indent=1)


write_to_file()