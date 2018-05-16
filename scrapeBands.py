import urllib
import urllib.request
import json

urlPrefix = "https://www.metal-archives.com/browse/ajax-letter/l/"
urlLetter = "Z"
urlSuffix = "/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart="
outputFile = urlLetter + "_Bands.txt"
url = urllib.request.urlopen(urlPrefix + urlLetter + urlSuffix + "0")


def GetRecNumberLine(lines):
    counter = 0
    for line in lines:
        if counter == 1:
            return line
        counter += 1


def GetRecNumber(line):
    for d in line.split():
        d = d.decode("utf-8").replace(",", "")
        if d.isdigit():
            return d


tmp = GetRecNumberLine(url)
result = []

def GetRecords():
    recNumber = int(GetRecNumber(tmp))
    counter = 0
    while counter < recNumber:
        with urllib.request.urlopen(urlPrefix + urlLetter + urlSuffix + str(counter)) as url:
            data = json.loads(url.read().decode())
            result.append(data['aaData'])
            counter += 500


GetRecords()


def WriteToFile():
    with open(outputFile, 'w') as outfile:   
        json.dump(result, outfile, indent=1)


WriteToFile()
