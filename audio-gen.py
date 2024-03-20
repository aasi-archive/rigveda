import json

GITHUB_BASE_URL = 'https://github.com/aasi-archive/rv-audio/raw/main/data'

verses_per_mandala = {}
rv_audio_json_data = {}

with open('rig-veda.json', encoding='utf-8') as f:
    RV_DATA = json.loads(''.join(f.readlines()))
    verses_per_mandala = RV_DATA["INFO_HEADER"]["VERSES_PER_MANDALA"]

def GenerateRawMP3Link(book, hymn):
    return f'{GITHUB_BASE_URL}/{book}/{hymn}.mp3'

for book in verses_per_mandala.keys():
    for hymn in range(1, verses_per_mandala[book] + 1):
        if book not in rv_audio_json_data:
            rv_audio_json_data[book] = {}
        rv_audio_json_data[book][hymn] = GenerateRawMP3Link(book, hymn)

with open('rig-veda-audio.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(rv_audio_json_data, indent=4))
    f.close()
