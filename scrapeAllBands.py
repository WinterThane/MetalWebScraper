from scrapeAlphabet import extract_letters
from scrapeBands import write_to_file
import time
import datetime


def write_all_files():
    letters = extract_letters()    
    for letter in letters:      
        print("Letter {0} started at: {1}".format(letter, datetime.datetime.now()))
        write_to_file(letter)
        print("Letter {0} ended at: {1}".format(letter, datetime.datetime.now()))
        time.sleep(10)


write_all_files()