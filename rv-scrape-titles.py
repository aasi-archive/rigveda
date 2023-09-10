import requests
from bs4 import BeautifulSoup
import re
import json

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

def GenerateMandalaURL_en(mandala):
    return f'https://sacred-texts.com/hin/rigveda/rvi{str(mandala).zfill(2)}.htm'

def GetMandalaIndex(mandala):
    req = requests.get(GenerateMandalaURL_en(mandala), headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup

def GetMandalaTitles(mandala):
    soup = GetMandalaIndex(mandala)
    anchors = soup.find_all('a', href=True)
    # Force one index
    title_array = [""]
    for anchor in anchors:
        if(anchor["href"].startswith("rv") and not anchor["href"].startswith("rvi")):
            title_array.append(anchor.get_text())

    return title_array

def LoadTitlesInJSON(mandala):
    title_array = GetMandalaTitles(mandala)
    for hymn in range(1, verses_per_mandala[mandala]+1):
        rigveda_json[str(mandala)][str(hymn)]["title"] = title_array[hymn]

with open("rv_full.json", "r", encoding='utf-8') as f:
     rigveda_json = json.loads(f.read())

for i in range(1, 10+1):
    print(f"Fetching title for Mandala {i}")
    LoadTitlesInJSON(i)

print("Writing the full data...")
with open("rv_full_with_titles.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(rigveda_json, ensure_ascii=False, indent=4))