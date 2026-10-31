# -*- coding: utf-8 -*-
"""Draws a picture of the focus tree: one icon per focus, one line per requirement."""
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, '/home/user/Marnix/tools/pdv_icons')
import layout

CELL = 44
ICON = 36
PAD = 60
LINE = {'cm': (196, 74, 66), 'dm': (96, 148, 214), 'fa': (200, 150, 70),
        'mo': (219, 178, 80), 'af': (143, 174, 98), 'nv': (86, 160, 200)}
TRUNK = (214, 202, 168)


def branch(fid):
    parts = fid.split('_')
    return parts[1] if len(parts) > 1 else ''


def main(out='/home/user/pdv_tree_preview.png'):
    cells, pre = layout.build()
    xs = [x for x, y in cells.values()]
    ys = [y for x, y in cells.values()]
    w = (max(xs) + 1) * CELL + PAD * 2
    h = (max(ys) + 1) * CELL + PAD * 2
    img = Image.new('RGB', (w, h), (24, 27, 33))
    d = ImageDraw.Draw(img, 'RGBA')

    def pos(fid):
        x, y = cells[fid]
        return PAD + x * CELL + CELL // 2, PAD + y * CELL + CELL // 2

    # edges first
    for fid, groups in pre.items():
        for g in groups:
            for p in g:
                col = LINE.get(branch(fid), TRUNK)
                d.line([pos(p), pos(fid)], fill=col + (150,), width=3)

    # icons
    for fid in cells:
        png = '/home/user/pdv_png/%s.png' % fid.lower()
        try:
            ic = Image.open(png).convert('RGBA').resize((ICON, ICON), Image.LANCZOS)
        except FileNotFoundError:
            ic = None
        cx, cy = pos(fid)
        if ic:
            img.paste(ic, (cx - ICON // 2, cy - ICON // 2), ic)
        else:
            d.ellipse([cx - ICON // 2, cy - ICON // 2, cx + ICON // 2, cy + ICON // 2],
                      fill=(58, 50, 34), outline=TRUNK, width=3)

    # labels
    for name, fid in (('COMMUNIST', 'PDV_cm_review'), ('DEMOCRATIC', 'PDV_dm_review'),
                      ('FASCIST', 'PDV_fa_review'), ('MONARCHIST', 'PDV_mo_review')):
        x, y = cells[fid]
        d.text((PAD + x * CELL + CELL // 2 - len(name) * 3, PAD + y * CELL - 26),
               name, fill=LINE[branch(fid)])
    d.text((PAD + 31 * CELL, PAD - 26), 'ARMY / AIR', fill=LINE['af'])
    d.text((PAD + 31 * CELL, PAD + 13 * CELL - 8), 'NAVY', fill=LINE['nv'])
    d.text((PAD + 14 * CELL - 30, PAD - 26), 'DIRECTORATE', fill=TRUNK)
    img.save(out)
    print(out, img.size)


if __name__ == '__main__':
    main()
