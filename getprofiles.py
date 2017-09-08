#!/usr/bin/python3

import time
import json
import requests
from bs4 import BeautifulSoup

profiles = {}

bdomain = 'https://soundcloud.com'
bdirsub = '/people/directory/'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}

request_stagger = 1.0

def setBS(char):
    global breq, bsoup
    breq = requests.get('{}{}{}'.format(bdomain,bdirsub,char), headers=headers, timeout=5).text
    bsoup = BeautifulSoup(breq,'lxml')

def set100(char):
    profiles[char] = []
    start = 1
    end = 100
    while True:
        print('Range: {} - {}'.format(start,end))
        req = requests.get('{}{}{}-{}-{}'.format(bdomain,bdirsub,char,start,end), headers=headers, timeout=5).text
        soup = BeautifulSoup(req,'lxml')
        select = soup.select('#app > noscript > div > ul > li > a > span:nth-of-type(2)')
        if select is None or len(select) == 0:
            break
        print('Working Profile Count: {}'.format(len(select)))
        for profile in select:
            profilename = '{}'.format(profile.contents[0])
            #print('Working Profile: {}'.format(profilename))
            profiles[char].append(profilename)
        start = start + 100
        end = end + 100
        # Stagger requests
        time.sleep(request_stagger)

# Per character...get profiles
setBS('A')
for charlink in bsoup.select('#app > noscript > ul > li a'):
    charhref = charlink.get('href')
    chartext = '{}'.format(charlink.contents[0])
    print('Working Character: {}'.format(chartext))
    set100(chartext)

# Save to JSON file
with open('profiles.json','w') as fp:
    json.dump(profiles, fp)
