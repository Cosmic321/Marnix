# -*- coding: utf-8 -*-
"""Draws a picture of the focus tree: one plate per focus, one line per requirement."""
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/home/user/Marnix/tools/pdv_icons')
import layout

CELL = 40
SIZE = 26
PAD = 70
LINE = {'cm': (196, 74, 66), 'dm': (96, 148, 214), 'fa': (200, 150, 70),
        'mo': (219, 178, 80), 'af': (143, 174, 98), 'nv': (86, 160, 200)}
TRUNK = (214, 202, 168)
HUB = ('review', 'spine1', 'spine2', 'spine3', 'spine4', 'spine5', 'spine6', 'final')


def branch(fid):
    parts = fid.split('_')
    return parts[1] if len(parts) > 1 else ''


def is_hub(fid):
    return fid.split('_')[-1] in HUB


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

    for fid, groups in pre.items():
        for g in groups:
            col = LINE.get(branch(fid), TRUNK)
            for p in g:
                d.line([pos(p), pos(fid)], fill=col + (140,), width=3)

    for fid in sorted(cells, key=lambda f: (is_hub(f), f)):
        cx, cy = pos(fid)
        col = LINE.get(branch(fid), TRUNK)
        if is_hub(fid):
            r = SIZE // 2 + 2
            d.regular_polygon((cx, cy, r), 4, rotation=45, fill=col + (235,),
                              outline=(16, 18, 22), width=2)
        else:
            r = SIZE // 2 - 2
            d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=5,
                                fill=col + (200,), outline=(16, 18, 22), width=2)

    for name, fid in (('COMMUNISM', 'PDV_cm_review'), ('DEMOCRACY', 'PDV_dm_review'),
                      ('FASCISM', 'PDV_fa_review'), ('MONARCHY', 'PDV_mo_review')):
        x, y = cells[fid]
        tw = len(name) * 6
        d.text((PAD + x * CELL + CELL // 2 - tw // 2, PAD + y * CELL - 14),
               name, fill=LINE[branch(fid)])
    d.text((PAD + layout.AF_X * CELL + CELL // 2 - 32, PAD - 34), 'ARMY / AIR', fill=LINE['af'])
    d.text((PAD + layout.NV_X * CELL + CELL // 2 - 16, PAD - 34), 'NAVY', fill=LINE['nv'])
    d.text((PAD + 15 * CELL - 30, PAD - 34), 'THE DIRECTORATE', fill=TRUNK)
    img.save(out)
    print(out, img.size)


if __name__ == '__main__':
    main()
