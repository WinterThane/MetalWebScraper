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


def make_filename(letter):
    if not letter:
        return "Z_Bands.txt"
    else:
        return (letter + "_Bands.txt")


urlPrefix = "https://www.metal-archives.com/browse/ajax-letter/l/"
urlSuffix = "/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart="


def make_url(letter):   
    if not letter:
        return (urlPrefix + "Z" + urlSuffix)
    else:
        return (urlPrefix + letter + urlSuffix)


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


result = []
output = []


def get_records(letter):
    url = make_url(letter)
    tmp = get_rec_number_line(urllib.request.urlopen(url + "0"))
    recNumber = int(get_rec_number(tmp))
    counter = 0
    while counter < recNumber:
        with urllib.request.urlopen(urlPrefix + letter + urlSuffix + str(counter)) as url:
            data = json.loads(url.read().decode())
            result.append(data['aaData'])
            counter += 500


def fix_band_name(nl):
    soup = BeautifulSoup(nl, "html.parser")
    name = soup.get_text()  
    for link in soup.find_all('a'):
        lnk = link.get('href')       
    return name, lnk


def make_new_json(letter):
    get_records(letter)   
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


def clean_lists():
    result.clear()
    output.clear()


def write_to_file(letter):
    make_new_json(letter)
    with open(make_filename(letter), 'w') as outfile:   
        json.dump(output, outfile, indent=1)
    clean_lists()


#if __name__ == '__main__':
    #outputFile = make_filename("Z")
    #write_to_file()