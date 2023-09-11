import json

with open('rig-veda.json', 'r', encoding='utf-8') as f:
    RV_JSON = json.loads(f.read())

RV_INDEX = {}

for mandala in range(1, 10+1):
    for hymn in range(1, RV_JSON["INFO_HEADER"]["VERSES_PER_MANDALA"][str(mandala)] + 1):
        RV_INDEX[f'{mandala}:{hymn}'] = RV_JSON[str(mandala)][str(hymn)]["EN"]

with open('rv_en.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(RV_INDEX, indent=4, ensure_ascii=False))
