# -*- coding: utf-8 -*-
"""Gives every state and every land province on the map a fictional name.

Three continents, three sounds: the Romance-speaking west (Swueltea), the hard
Germanic/Slavic centre (Aind) and the vowel-heavy south (Iochoapp). Names are
generated once and cached in tools/pdv_icons/world_names.json so re-runs do not
reshuffle the map under the other files that refer to it.
"""
import csv
import json
import os
import random
import re

ROOT = '/home/user/Marnix/CosmicDaWinner/'
CACHE = '/home/user/Marnix/tools/pdv_icons/world_names.json'

# ---------------------------------------------------------------- phonologies
PHON = {
    '1': {   # Swueltea
        'onset': ['b', 'c', 'd', 'f', 'g', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v',
                  'br', 'dr', 'gr', 'pr', 'tr', 'cl', 'fl'],
        'nucleus': ['a', 'e', 'i', 'o', 'u', 'ai', 'ei', 'ia', 'io'],
        'coda': ['', '', '', 'l', 'n', 'r', 's', 'm'],
        'tail': ['a', 'o', 'e', 'ia', 'ano', 'eno', 'ora', 'aro', 'ino', 'esa'],
    },
    '2': {   # Aind
        'onset': ['b', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'r', 's', 't', 'v',
                  'br', 'dr', 'gr', 'kr', 'st', 'vl', 'sk', 'th'],
        'nucleus': ['a', 'e', 'i', 'o', 'u', 'au', 'ei', 'ie', 'ou'],
        'coda': ['', '', 'r', 'n', 'l', 's', 'm', 'k', 't'],
        'tail': ['berg', 'wald', 'ov', 'in', 'sk', 'heim', 'dorf', 'grad', 'au', 'mark'],
    },
    '3': {   # Iochoapp
        'onset': ['h', 'j', 'k', 'l', 'm', 'n', 's', 't', 'w', 'v', 'hl', 'kw', 'sh'],
        'nucleus': ['a', 'e', 'i', 'o', 'u', 'oa', 'ua', 'io', 'ai', 'ea'],
        'coda': ['', '', '', '', 'n', 'l', 's'],
        'tail': ['oa', 'ai', 'ua', 'io', 'ea', 'oan', 'uan', 'aia'],
    },
    '0': {'onset': ['b', 'k', 'l', 'm', 'n', 'r', 's', 't', 'v'],
          'nucleus': ['a', 'e', 'i', 'o', 'u'],
          'coda': ['', '', 'n', 'r', 'l'],
          'tail': ['a', 'o', 'en', 'ar']},
}


def make_name(rng, region, used):
    """Two or three clean syllables, then a regional ending."""
    ph = PHON.get(region, PHON['0'])
    for _ in range(80):
        count = rng.choice([2, 2, 2, 3])
        parts = []
        for i in range(count):
            onset = rng.choice(ph['onset'])
            nucleus = rng.choice(ph['nucleus'])
            while len(nucleus) > 1 and i < count - 1 and rng.random() < 0.7:
                nucleus = rng.choice([n for n in ph['nucleus'] if len(n) == 1])
            coda = rng.choice(ph['coda']) if (i == count - 1 or rng.random() < 0.25) else ''
            parts.append(onset + nucleus + coda)
        word = ''.join(parts)
        word = re.sub(r'([aeiou])\1+', r'\1', word)
        if rng.random() < 0.55:
            tail = rng.choice(ph['tail'])
            if tail[0] in 'aeiou' and word[-1] in 'aeiou':
                word = word[:-1]
            word += tail
        word = re.sub(r'([aeiou])\1+', r'\1', word)
        word = word.capitalize()
        if len(word) < 4 or len(word) > 13 or word in used:
            continue
        if re.search(r'(.{2,4})\1', word.lower()):   # no "gragrane" stutter
            continue
        used.add(word)
        return word
    while True:
        word = 'V' + str(rng.randint(1000, 9999))
        if word not in used:
            used.add(word)
            return word


def build():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, encoding='utf-8'))

    rng = random.Random(19370101)
    rows = [r for r in csv.reader(open(ROOT + 'map/definition.csv', encoding='utf-8-sig'),
                                  delimiter=';') if r and r[0].isdigit()]
    land = [(int(r[0]), r[7]) for r in rows if r[4] == 'land']

    used = set()
    provinces = {str(pid): make_name(rng, region, used) for pid, region in land}

    # a state takes its region from its own provinces
    states = {}
    for f in sorted(os.listdir(ROOT + 'history/states')):
        if not f.endswith('.txt'):
            continue
        s = open(ROOT + 'history/states/' + f, encoding='utf-8-sig').read()
        sid = re.search(r'id\s*=\s*(\d+)', s).group(1)
        provs = re.findall(r'\b(\d{1,5})\b', s.split('provinces')[1].split('}')[0]) \
            if 'provinces' in s else []
        regions = [provinces[p] for p in provs if p in provinces]  # names, not regions
        region = '0'
        for p in provs:
            for pid, rg in land:
                if str(pid) == p:
                    region = rg
                    break
            else:
                continue
            break
        states[sid] = make_name(rng, region, used)

    data = {'provinces': provinces, 'states': states}
    json.dump(data, open(CACHE, 'w', encoding='utf-8'), indent=0, sort_keys=True)
    return data


def write_loc(data):
    state_path = ROOT + 'localisation/english/replace/state_names_l_english.yml'
    out = ['l_english:']
    for sid, name in sorted(data['states'].items(), key=lambda kv: int(kv[0])):
        out.append(' STATE_%s:0 "%s"' % (sid, name))
    open(state_path, 'w', encoding='utf-8-sig', newline='\n').write('\n'.join(out) + '\n')

    prov_path = ROOT + 'localisation/english/replace/province_names_l_english.yml'
    out = ['l_english:']
    for pid, name in sorted(data['provinces'].items(), key=lambda kv: int(kv[0])):
        out.append(' PROV%s:0 "%s"' % (pid, name))
    open(prov_path, 'w', encoding='utf-8-sig', newline='\n').write('\n'.join(out) + '\n')
    print('states:', len(data['states']), 'provinces:', len(data['provinces']))


if __name__ == '__main__':
    write_loc(build())
