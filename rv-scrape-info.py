import requests
import json

with open('rig-veda.json', 'r', encoding='utf-8') as f:
    RV = json.loads(f.read())
with open('stanzas-per-verse.json', 'r') as f:
    RV_STANZAS_PER_VERSE = json.loads(f.read())

RV_INFO_JSON = {}
def GetRVVedaWebURL(mandala, hymn, stanza):
    mandala_s = str(mandala).zfill(2)
    hymn_s = str(hymn).zfill(3)
    stanza_s = str(stanza).zfill(2)
    return f'https://vedaweb.uni-koeln.de/rigveda/api/document/id/{mandala_s}{hymn_s}{stanza_s}'

def GetRVJSON(mandala, hymn, stanza):
    response = requests.get(GetRVVedaWebURL(mandala, hymn, stanza))
    return response.json()

def RVGetHymnMax(mandala):
    return RV["INFO_HEADER"]["VERSES_PER_MANDALA"][str(mandala)]

def RVGetStanzaMax(mandala, hymn):
    return RV_STANZAS_PER_VERSE[str(mandala)][str(hymn)]

for mandala in range(9, 10+1):
    for hymn in range(1, RVGetHymnMax(mandala)+1):
        print(f"Fetching info for {mandala}.{hymn}")
        if(mandala not in RV_INFO_JSON):
            RV_INFO_JSON[mandala] = {}
        
        vedaweb_info = GetRVJSON(mandala, hymn, 1)
        RV_INFO_JSON[mandala][hymn] = { 
            "stanzas": RVGetStanzaMax(mandala, hymn),
            "group": vedaweb_info["hymnGroup"]
        }
    with open('rig-veda-verse-info.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(RV_INFO_JSON, indent=4, ensure_ascii=False))