import json
import os
import jinja2
import re
import colorama

RV_BUILD_DIR = './build/'
with open('rig-veda.json', 'r', encoding='utf-8') as f:
    RV_DATA = json.loads(f.read())
with open('rig-veda-audio.json', 'r') as f:
    RV_AUDIO_DATA = json.loads(f.read())

template_loader = jinja2.FileSystemLoader(searchpath="./")
template_engine = jinja2.Environment(loader=template_loader)
hymn_template = template_engine.get_template("hymn.template.html")
mandala_template = template_engine.get_template("mandala.template.html")
verse_english_line_splitter = re.compile(r'^\d+\s', flags=re.MULTILINE | re.DOTALL)
verse_sanskrit_line_splitter = re.compile(r'(\|\|)', flags=re.MULTILINE | re.DOTALL)

def GetRVHymn(mandala, hymn):
    return RV_DATA[str(mandala)][str(hymn)]

def GetRVHymnAudioURL(mandala, hymn):
    try:
        return RV_AUDIO_DATA[str(mandala)][str(hymn)]
    except:
        import traceback
        print(traceback.format_exc())

def GetRVMandalaMax(mandala):
    return RV_DATA["INFO_HEADER"]["VERSES_PER_MANDALA"][str(mandala)]

def GetRVMandalaTitles(mandala):
    titles = []
    mandala_max = GetRVMandalaMax(mandala)
    for i in range(1, mandala_max+1):
        icon = "hymn"
        title = GetRVHymn(mandala, i)["title"]
        title = re.split('HYMN ([IVXLCDM]+)', title)[2]
        title = title.replace(".", "")
        title = title.strip()

        if("Maruts" in title):
            icon = "maruts"
        if("Āprīs" in title):
            icon = "apris"
        if("Aśvins" in title):
            icon = "asvin"
        if("Vāyu" in title):
            icon = "vayu"
        if("Varuṇa" in title):
            icon = "varuna"
        if("Sūrya" in title):
            icon = "surya"
        if("Agni" in title):
            icon = "agni"
        if("Rudra" in title):
            icon = "rudra"
        if("Indra" in title):
            icon = "indra"

        titles.append({ "title": title, "icon": icon })
    return titles

def GenerateRVHymnPath(mandala, hymn, prefix=RV_BUILD_DIR):
    return os.path.join(prefix, f'{mandala}/{hymn}.html')

def GenerateRVMandalaPath(mandala, prefix=RV_BUILD_DIR):
    return os.path.join(prefix, f'{mandala}/index.html')

def RenderRVMandalaIndex(mandala):
    file_path = GenerateRVMandalaPath(mandala)
    file_dir = os.path.dirname(file_path)
    os.makedirs(file_dir, exist_ok=True)
    hymn_titles = GetRVMandalaTitles(mandala)
    next_mandala = ''
    prev_mandala = ''

    if(mandala < 10):
        next_mandala = GenerateRVMandalaPath(mandala+1, prefix='')
    if(mandala > 1):
        prev_mandala = GenerateRVMandalaPath(mandala-1, prefix='')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(mandala_template.render({ 
            'hymns': hymn_titles,
            'mandala': mandala,
            'next_mandala': next_mandala,
            'prev_mandala': prev_mandala
        }))

def RenderRVHymn(mandala, hymn):
    file_path = GenerateRVHymnPath(mandala, hymn)
    file_dir = os.path.dirname(file_path)
    os.makedirs(file_dir, exist_ok=True)

    hymn_data = GetRVHymn(mandala, hymn)
    previous_page_url = ''
    next_page_url = ''
    
    max_mandalas = 10
    max_hymns = GetRVMandalaMax(mandala)

    if(hymn < max_hymns):
        next_page_url = GenerateRVHymnPath(mandala, hymn+1, '')
    if(hymn == max_hymns and mandala < max_mandalas):
        next_page_url = GenerateRVHymnPath(mandala+1, 1, '')
    
    if(hymn > 1):
        previous_page_url = GenerateRVHymnPath(mandala, hymn-1, '')
    if(hymn == 1 and mandala > 1):
        previous_page_url = GenerateRVHymnPath(mandala-1, GetRVMandalaMax(mandala-1), '')

    with open(file_path, 'w', encoding='utf-8') as f:
        # Prepare Hymn lines
        hymn_lines = []
        try:
            # Split by ||
            hymn_lines_sanskrit = re.split(verse_sanskrit_line_splitter, hymn_data["SA"])
            hymn_lines_sanskrit = [item for item in hymn_lines_sanskrit if item.strip()]
            # Joint || to the previous
            hymn_lines_sanskrit = [hymn_lines_sanskrit[i] + hymn_lines_sanskrit[i+1] for i in range(0, len(hymn_lines_sanskrit), 2)]
            # Extract transliteration
            hymn_lines_transliteration = re.split(verse_sanskrit_line_splitter, hymn_data["SA_R"])
            hymn_lines_transliteration = [item for item in hymn_lines_transliteration if item.strip()]
            hymn_lines_transliteration = [hymn_lines_transliteration[i] + hymn_lines_transliteration[i+1] for i in range(0, len(hymn_lines_transliteration), 2)]
            # Extract English Translation
            hymn_lines_english = re.split(verse_english_line_splitter, hymn_data["EN"])
            hymn_lines_english = [item for item in hymn_lines_english if item.strip()]
            n = len(hymn_lines_sanskrit)

            print(len(hymn_lines_sanskrit), len(hymn_lines_english), len(hymn_lines_transliteration))
            for i in range(0, n):
                hymn_lines.append({ "SA": hymn_lines_sanskrit[i].strip().replace('\n', ' <br> '), "EN": hymn_lines_english[i].strip().replace('\n', ' <br> '), "SA_R": hymn_lines_transliteration[i].strip().replace('\n', ' <br> ') })
            
            # Add links to learnsanskrit.cc to every html
            for idx, stanza in enumerate(hymn_lines):
                sa_text = stanza["SA"]
                translit = stanza["SA_R"]
                sanskrit_words = sa_text.split(' ')
                translit_words = translit.split(' ')

                if(len(sanskrit_words) != len(translit_words)):
                    print(sanskrit_words)
                    print(translit_words)
                    input("Transliteration seems messed up. ENTER to Continue.")
                
                sanskrit_words_with_links = []
                for iword, word in enumerate(sanskrit_words):
                    if(not word.startswith('<') and not word.startswith('|')):
                        sanskrit_words_with_links.append(f'<a class="sanskrit-word" target="_blank" href="https://www.learnsanskrit.cc/translate?search={word}">{word}<span class="transliteration-word">{translit_words[iword]}</span></a>')
                    else:
                        if(word == '<br>'):
                            word += '<br>'
                        sanskrit_words_with_links.append(word)

                sa_text = ' '.join(sanskrit_words_with_links)
                hymn_lines[idx]["SA"] = sa_text

            f.write(hymn_template.render({ 
                'hymn_lines': hymn_lines, 
                'mandala': mandala, 
                'hymn': hymn, 
                'hymn_title': hymn_data["title"].upper(),
                'next_page_url': next_page_url,
                'previous_page_url': previous_page_url,
                'audio_url': GetRVHymnAudioURL(mandala, hymn)
            }))
        except:
            print(colorama.Fore.RED + "FAILED!" + colorama.Fore.RESET)


for mandala in range(1, 10+1):
    MANDALA_MAX = GetRVMandalaMax(mandala)
    for hymn in range(1, MANDALA_MAX+1):
        print(f"Generating hymn {mandala}.{hymn}")
        RenderRVHymn(mandala, hymn)
    RenderRVMandalaIndex(mandala)