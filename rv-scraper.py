import requests
from bs4 import BeautifulSoup
import re
import json
from time import sleep

rigveda_json = {}

sanskrit_text_search = re.compile(r'</h3>(.*?)<p>', re.MULTILINE | re.DOTALL)
romanization_text_search = re.compile(r'</p>(.*?)<hr/>', re.MULTILINE | re.DOTALL)

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

verses_per_mandala = {
    1: 191,
    2: 43,
    3: 62,
    4: 58,
    5: 87,
    6: 75,
    7: 104,
    8: 103,
    9: 114,
    10: 190
}

def StripLeadingSpaces(multiline_string):
    # Split the string into lines
    lines = multiline_string.split('\n')
    # Join the lines back into a single string
    return '\n'.join([line.strip() for line in lines])

def GenerateRVURL_en(mandala, hymn):
    return f'https://sacred-texts.com/hin/rigveda/rv{str(mandala).zfill(2)}{str(hymn).zfill(3)}.htm'

def GenerateRVURL_sa(mandala, hymn):
    return f'https://sacred-texts.com/hin/rvsan/rv{str(mandala).zfill(2)}{str(hymn).zfill(3)}.htm'


def GetSanskritHymn(mandala, hymn):
    req = requests.get(GenerateRVURL_sa(mandala,hymn), headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    soup_string = str(soup)
    sanskrit_text = StripLeadingSpaces(re.search(sanskrit_text_search, soup_string).group(1).replace("<br/>", "").strip())
    roman_text = StripLeadingSpaces(re.search(romanization_text_search, soup_string).group(1).replace("<br/>", "").replace("<p>", "").strip())
    return (sanskrit_text, roman_text)

def GetEnglishHymn(mandala, hymn):
    req = requests.get(GenerateRVURL_en(mandala,hymn), headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    paragraphs = soup.find_all('p')
    english_text = StripLeadingSpaces(paragraphs[1].get_text(separator="\n").strip())
    return english_text

def GetHymn(mandala, hymn):
    if(mandala not in rigveda_json):
        rigveda_json[mandala] = {}
    
    rigveda_json[mandala][hymn] = {}

    print(f"Fetching Mandala {mandala}, Hymn {hymn}")
    ENG = GetEnglishHymn(mandala,hymn)
    SA, SA_R = GetSanskritHymn(mandala,hymn)

    rigveda_json[mandala][hymn]["EN"] = ENG
    rigveda_json[mandala][hymn]["SA"] = SA
    rigveda_json[mandala][hymn]["SA_R"] = SA_R

for mandala in verses_per_mandala.keys():
    for hymn in range(1, verses_per_mandala[mandala]+1):
        GetHymn(mandala, hymn)
    print(f"Writing Mandala {mandala}...")
    with open(f'rv_{mandala}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(rigveda_json, indent=4, ensure_ascii=False))
