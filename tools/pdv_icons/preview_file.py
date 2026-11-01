# -*- coding: utf-8 -*-
"""Renders whatever is actually in PDV_vyratia.txt: positions, prerequisites,
mutual exclusions. Read-only, so it is safe to run against a hand-edited tree."""
import re
import sys
from PIL import Image, ImageDraw

TREE = '/home/user/Marnix/CosmicDaWinner/common/national_focus/PDV_vyratia.txt'
OUT = '/home/user/pdv_tree_preview.png'
CELL = 34
PAD = 70
LINE = (150, 170, 200)
MUTEX = (200, 80, 70)


def blocks(src):
    out, i = [], 0
    while True:
        j = src.find('\tfocus = {', i)
        if j < 0:
            return out
        k = src.index('{', j)
        depth, m = 0, k
        while True:
            c = src[m]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
            m += 1
        out.append(src[j:m + 1])
        i = m + 1


def main():
    s = open(TREE, encoding='utf-8-sig').read()
    cells, pre, mut = {}, {}, {}
    for b in blocks(s):
        fid = re.search(r'\tid = (\w+)', b).group(1)
        cells[fid] = (int(re.search(r'\tx = (\d+)', b).group(1)),
                      int(re.search(r'\ty = (\d+)', b).group(1)))
        pre[fid] = re.findall(r'prerequisite = \{ focus = (\w+)', b)
        mut[fid] = re.findall(r'mutually_exclusive = \{ focus = (\w+)', b)

    xs = [x for x, y in cells.values()]
    ys = [y for x, y in cells.values()]
    img = Image.new('RGB', ((max(xs) + 2) * CELL + PAD, (max(ys) + 2) * CELL + PAD), (24, 27, 33))
    d = ImageDraw.Draw(img, 'RGBA')

    def pos(f):
        x, y = cells[f]
        return PAD + x * CELL + CELL // 2, PAD + y * CELL + CELL // 2

    for f, ps in pre.items():
        for p in ps:
            if p in cells:
                d.line([pos(p), pos(f)], fill=LINE + (110,), width=2)
    for f, ms in mut.items():
        for m in ms:
            if m in cells:
                d.line([pos(f), pos(m)], fill=MUTEX + (110,), width=2)

    econ = ('PDV_econ_patient', 'PDV_econ_step1', 'PDV_econ_step2', 'PDV_econ_step3',
            'PDV_econ_force', 'PDV_print_money', 'PDV_generals_power', 'PDV_propaganda_supremacy')
    for f in cells:
        cx, cy = pos(f)
        r = 11
        if f in econ:
            d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=4,
                                fill=(228, 196, 120, 245), outline=(255, 240, 200), width=2)
        else:
            d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=3,
                                fill=(70, 84, 110, 235), outline=(20, 22, 28), width=1)

    for f in econ:
        x, y = cells[f]
        d.text((PAD + x * CELL - 6, PAD + y * CELL + CELL), f.replace('PDV_', ''), fill=(228, 196, 120))
    img.save(OUT)
    print(OUT, img.size, len(cells), 'focuses')


if __name__ == '__main__':
    main()
