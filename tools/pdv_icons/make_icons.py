# -*- coding: utf-8 -*-
"""Generates the custom Vyratia focus icons (68x68 DDS) plus their sprite definitions."""
import math, os, re, subprocess
from PIL import Image, ImageDraw

MOD = '/home/user/Marnix/CosmicDaWinner/'
OUT = MOD + 'gfx/interface/goals/pdv/'
S = 272          # supersampled canvas
F = S / 68.0     # scale factor

IVORY = (243, 233, 202, 255)


def P(pts):
    return [(S * x, S * y) for x, y in pts]


def W(mult=1.0):
    return max(1, int(4.6 * F * mult))
SHADOW = (0, 0, 0, 110)

PALETTE = {
    'cm': ((92, 26, 26), (34, 10, 10), (210, 66, 54)),
    'dm': ((28, 46, 84), (12, 20, 38), (96, 148, 214)),
    'fa': ((62, 48, 34), (24, 18, 12), (186, 138, 62)),
    'mo': ((78, 48, 20), (28, 16, 8), (219, 178, 80)),
    'af': ((44, 58, 36), (18, 24, 14), (143, 174, 98)),
    'nv': ((26, 46, 62), (10, 18, 26), (86, 160, 200)),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def plate(shape, pal):
    """Dark bevelled plate with a bright rim."""
    top, bot, accent = pal
    mask = Image.new('L', (S, S), 0)
    md = ImageDraw.Draw(mask)
    m = S * 0.06
    if shape == 'circle':
        md.ellipse([m, m, S - m, S - m], fill=255)
    elif shape == 'shield':
        md.polygon([(m, m), (S - m, m), (S - m, S * 0.58), (S / 2, S - m), (m, S * 0.58)], fill=255)
    elif shape == 'diamond':
        md.polygon([(S / 2, m), (S - m, S / 2), (S / 2, S - m), (m, S / 2)], fill=255)
    else:  # rounded square
        md.rounded_rectangle([m, m, S - m, S - m], radius=S * 0.14, fill=255)

    grad = Image.new('RGB', (S, S))
    gd = ImageDraw.Draw(grad)
    for y in range(S):
        gd.line([(0, y), (S, y)], fill=lerp(top, bot, y / (S - 1.0)))
    plate_img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    plate_img.paste(grad, (0, 0), mask)

    rim = Image.new('L', (S, S), 0)
    rd = ImageDraw.Draw(rim)
    w = int(3.2 * F)
    if shape == 'circle':
        rd.ellipse([m, m, S - m, S - m], outline=255, width=w)
        rd.ellipse([m + w * 2, m + w * 2, S - m - w * 2, S - m - w * 2], outline=170, width=max(1, w // 2))
    elif shape == 'shield':
        rd.line([(m, m), (S - m, m), (S - m, S * 0.58), (S / 2, S - m), (m, S * 0.58), (m, m)],
                fill=255, width=w, joint='curve')
    elif shape == 'diamond':
        rd.line([(S / 2, m), (S - m, S / 2), (S / 2, S - m), (m, S / 2), (S / 2, m)], fill=255, width=w, joint='curve')
    else:
        rd.rounded_rectangle([m, m, S - m, S - m], radius=S * 0.14, outline=255, width=w)
    rim_img = Image.new('RGBA', (S, S), (176, 141, 63, 255))
    plate_img.paste(rim_img, (0, 0), rim)

    acc = Image.new('RGBA', (S, S), accent + (255,))
    path = Image.new('L', (S, S), 0)
    pd = ImageDraw.Draw(path)
    if shape == 'circle':
        pd.arc([m + w * 3, m + w * 3, S - m - w * 3, S - m - w * 3], 200, 340, fill=255, width=max(2, w // 2))
    else:
        pd.line([(S * 0.22, S * 0.86), (S * 0.78, S * 0.86)], fill=255, width=max(2, int(2.4 * F)))
    plate_img.paste(acc, (0, 0), path)
    return plate_img


# ---------------------------------------------------------------- glyphs
def g_hammer_sickle(d):
    w = int(4.4 * F)
    # sickle: thick crescent arc opening up-left
    d.arc([S * 0.22, S * 0.26, S * 0.78, S * 0.82], 200, 20, fill=IVORY, width=w)
    d.line([(S * 0.72, S * 0.30), (S * 0.62, S * 0.40)], fill=IVORY, width=w)
    # hammer crossing it
    d.line([(S * 0.30, S * 0.74), (S * 0.62, S * 0.34)], fill=IVORY, width=int(3.6 * F))
    d.polygon([(S * 0.56, S * 0.20), (S * 0.74, S * 0.34), (S * 0.64, S * 0.44), (S * 0.46, S * 0.30)], fill=IVORY)


def g_cog(d):
    cx = cy = S / 2
    r = S * 0.22
    for i in range(8):
        a = i * math.pi / 4
        x1, y1 = cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8
        x2, y2 = cx + math.cos(a) * r * 1.35, cy + math.sin(a) * r * 1.35
        d.line([(x1, y1), (x2, y2)], fill=IVORY, width=int(5 * F))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=IVORY, width=int(5 * F))
    d.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35], fill=IVORY)


def g_star(d):
    cx = cy = S / 2
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = S * (0.30 if i % 2 == 0 else 0.125)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=IVORY)


def g_crown(d):
    d.rectangle([S * 0.24, S * 0.56, S * 0.76, S * 0.66], fill=IVORY)
    for i in range(3):
        x = S * (0.30 + i * 0.20)
        d.polygon([(x - S * 0.075, S * 0.56), (x, S * 0.26), (x + S * 0.075, S * 0.56)], fill=IVORY)
    d.rectangle([S * 0.24, S * 0.70, S * 0.76, S * 0.75], fill=IVORY)


def g_fasces(d):
    for i in range(5):
        x = S * (0.40 + i * 0.045)
        d.line([(x, S * 0.30), (x, S * 0.74)], fill=IVORY, width=int(2.6 * F))
    d.line([(S * 0.34, S * 0.40), (S * 0.34, S * 0.70)], fill=IVORY, width=int(3 * F))
    d.polygon([(S * 0.60, S * 0.26), (S * 0.74, S * 0.34), (S * 0.60, S * 0.44)], fill=IVORY)


def g_ballot(d):
    d.rectangle([S * 0.28, S * 0.48, S * 0.72, S * 0.76], outline=IVORY, width=int(3.4 * F))
    d.rectangle([S * 0.40, S * 0.52, S * 0.60, S * 0.56], fill=IVORY)
    d.polygon([(S * 0.42, S * 0.46), (S * 0.58, S * 0.46), (S * 0.58, S * 0.24), (S * 0.42, S * 0.24)], fill=IVORY)
    d.line([(S * 0.46, S * 0.30), (S * 0.54, S * 0.30)], fill=(0, 0, 0, 120), width=int(1.6 * F))
    d.line([(S * 0.46, S * 0.36), (S * 0.54, S * 0.36)], fill=(0, 0, 0, 120), width=int(1.6 * F))


def g_tank(d):
    d.rounded_rectangle([S * 0.20, S * 0.50, S * 0.80, S * 0.68], radius=S * 0.03, fill=IVORY)
    d.rounded_rectangle([S * 0.34, S * 0.36, S * 0.62, S * 0.52], radius=S * 0.02, fill=IVORY)
    d.line([(S * 0.62, S * 0.42), (S * 0.84, S * 0.42)], fill=IVORY, width=int(3.4 * F))
    for i in range(4):
        cx = S * (0.28 + i * 0.15)
        d.ellipse([cx - S * 0.045, S * 0.60 - S * 0.045, cx + S * 0.045, S * 0.60 + S * 0.045],
                  outline=(0, 0, 0, 130), width=int(1.6 * F))


def g_plane(d):
    d.polygon([(S * 0.50, S * 0.20), (S * 0.56, S * 0.44), (S * 0.80, S * 0.56), (S * 0.80, S * 0.63),
               (S * 0.56, S * 0.58), (S * 0.57, S * 0.74), (S * 0.66, S * 0.80), (S * 0.66, S * 0.84),
               (S * 0.50, S * 0.80), (S * 0.34, S * 0.84), (S * 0.34, S * 0.80), (S * 0.43, S * 0.74),
               (S * 0.44, S * 0.58), (S * 0.20, S * 0.63), (S * 0.20, S * 0.56), (S * 0.44, S * 0.44)],
              fill=IVORY)


def g_ship(d):
    d.polygon([(S * 0.18, S * 0.58), (S * 0.82, S * 0.58), (S * 0.72, S * 0.74), (S * 0.28, S * 0.74)], fill=IVORY)
    d.rectangle([S * 0.38, S * 0.42, S * 0.62, S * 0.58], fill=IVORY)
    d.rectangle([S * 0.46, S * 0.28, S * 0.52, S * 0.44], fill=IVORY)
    for i in range(3):
        d.arc([S * (0.14 + i * 0.24), S * 0.72, S * (0.36 + i * 0.24), S * 0.86], 180, 360,
              fill=IVORY, width=int(2.4 * F))


def g_anchor(d):
    d.line([(S * 0.50, S * 0.28), (S * 0.50, S * 0.74)], fill=IVORY, width=int(3.6 * F))
    d.line([(S * 0.34, S * 0.38), (S * 0.66, S * 0.38)], fill=IVORY, width=int(3.2 * F))
    d.ellipse([S * 0.44, S * 0.18, S * 0.56, S * 0.30], outline=IVORY, width=int(3 * F))
    d.arc([S * 0.24, S * 0.46, S * 0.76, S * 0.84], 20, 160, fill=IVORY, width=int(3.6 * F))
    d.polygon([(S * 0.24, S * 0.60), (S * 0.34, S * 0.66), (S * 0.26, S * 0.72)], fill=IVORY)
    d.polygon([(S * 0.76, S * 0.60), (S * 0.66, S * 0.66), (S * 0.74, S * 0.72)], fill=IVORY)


def g_factory(d):
    d.polygon([(S * 0.18, S * 0.74), (S * 0.18, S * 0.46), (S * 0.36, S * 0.56), (S * 0.36, S * 0.46),
               (S * 0.54, S * 0.56), (S * 0.54, S * 0.46), (S * 0.72, S * 0.56), (S * 0.72, S * 0.74)], fill=IVORY)
    d.rectangle([S * 0.66, S * 0.24, S * 0.74, S * 0.52], fill=IVORY)


def g_wheat(d):
    d.line([(S * 0.50, S * 0.78), (S * 0.50, S * 0.26)], fill=IVORY, width=int(2.6 * F))
    for i in range(4):
        y = S * (0.34 + i * 0.11)
        for sgn in (-1, 1):
            d.ellipse([S * 0.50 + sgn * S * 0.02 - (S * 0.06 if sgn > 0 else 0),
                       y, S * 0.50 + sgn * S * 0.02 + (S * 0.06 if sgn < 0 else 0), y + S * 0.07], fill=IVORY)


def g_book(d):
    d.polygon([(S * 0.52, S * 0.30), (S * 0.82, S * 0.38), (S * 0.82, S * 0.68), (S * 0.52, S * 0.60)], fill=IVORY)
    d.polygon([(S * 0.48, S * 0.30), (S * 0.18, S * 0.38), (S * 0.18, S * 0.68), (S * 0.48, S * 0.60)], fill=IVORY)
    for i in range(3):
        y = S * (0.42 + i * 0.09)
        d.line([(S * 0.26, y), (S * 0.44, y + S * 0.02)], fill=(0, 0, 0, 90), width=int(1.6 * F))
        d.line([(S * 0.56, y + S * 0.02), (S * 0.74, y)], fill=(0, 0, 0, 90), width=int(1.6 * F))


def g_radio(d):
    d.line([(S * 0.50, S * 0.74), (S * 0.50, S * 0.34)], fill=IVORY, width=int(3 * F))
    d.line([(S * 0.36, S * 0.74), (S * 0.50, S * 0.34)], fill=IVORY, width=int(2 * F))
    d.line([(S * 0.64, S * 0.74), (S * 0.50, S * 0.34)], fill=IVORY, width=int(2 * F))
    d.ellipse([S * 0.44, S * 0.26, S * 0.56, S * 0.38], fill=IVORY)
    for i, r in enumerate((S * 0.16, S * 0.24)):
        d.arc([S / 2 - r, S * 0.32 - r * 0.6, S / 2 + r, S * 0.32 + r * 1.4], 200, 340,
              fill=IVORY, width=int(2 * F))


def g_torch(d):
    d.line([(S * 0.50, S * 0.80), (S * 0.50, S * 0.50)], fill=IVORY, width=int(4 * F))
    d.polygon([(S * 0.42, S * 0.52), (S * 0.58, S * 0.52), (S * 0.54, S * 0.44), (S * 0.46, S * 0.44)], fill=IVORY)
    d.polygon([(S * 0.50, S * 0.18), (S * 0.62, S * 0.38), (S * 0.50, S * 0.46), (S * 0.38, S * 0.38)], fill=IVORY)


def g_sword(d):
    d.polygon([(S * 0.50, S * 0.16), (S * 0.56, S * 0.30), (S * 0.56, S * 0.62), (S * 0.44, S * 0.62),
               (S * 0.44, S * 0.30)], fill=IVORY)
    d.line([(S * 0.30, S * 0.62), (S * 0.70, S * 0.62)], fill=IVORY, width=int(4 * F))
    d.line([(S * 0.50, S * 0.62), (S * 0.50, S * 0.80)], fill=IVORY, width=int(3.4 * F))


def g_shield(d):
    d.polygon([(S * 0.24, S * 0.28), (S * 0.76, S * 0.28), (S * 0.76, S * 0.56), (S * 0.50, S * 0.78),
               (S * 0.24, S * 0.56)], outline=IVORY, width=int(4 * F))
    d.line([(S * 0.50, S * 0.40), (S * 0.50, S * 0.62)], fill=IVORY, width=int(3 * F))


def g_castle(d):
    d.rectangle([S * 0.26, S * 0.46, S * 0.74, S * 0.76], fill=IVORY)
    for x in (S * 0.26, S * 0.50, S * 0.74 - S * 0.08):
        d.rectangle([x, S * 0.34, x + S * 0.08, S * 0.50], fill=IVORY)
    d.rectangle([S * 0.46, S * 0.58, S * 0.54, S * 0.76], fill=(0, 0, 0, 140))


def g_train(d):
    d.rounded_rectangle([S * 0.24, S * 0.34, S * 0.68, S * 0.66], radius=S * 0.04, fill=IVORY)
    d.rectangle([S * 0.66, S * 0.46, S * 0.78, S * 0.66], fill=IVORY)
    for cx in (S * 0.34, S * 0.48, S * 0.62, S * 0.74):
        d.ellipse([cx - S * 0.055, S * 0.64, cx + S * 0.055, S * 0.75], fill=IVORY)
    d.line([(S * 0.18, S * 0.80), (S * 0.84, S * 0.80)], fill=IVORY, width=int(2.4 * F))


def g_derrick(d):
    d.polygon([(S * 0.50, S * 0.20), (S * 0.72, S * 0.76), (S * 0.62, S * 0.76), (S * 0.50, S * 0.36),
               (S * 0.38, S * 0.76), (S * 0.28, S * 0.76)], fill=IVORY)
    d.line([(S * 0.34, S * 0.62), (S * 0.66, S * 0.62)], fill=IVORY, width=int(2.2 * F))
    d.line([(S * 0.40, S * 0.48), (S * 0.60, S * 0.48)], fill=IVORY, width=int(2.2 * F))


def g_pickaxe(d):
    d.line([(S * 0.24, S * 0.84), (S * 0.66, S * 0.30)], fill=IVORY, width=W(0.85))
    d.arc([S * 0.16, S * 0.12, S * 0.92, S * 0.62], 195, 345, fill=IVORY, width=W(0.9))
    d.polygon(P([(0.14, 0.44), (0.24, 0.30), (0.30, 0.46)]), fill=IVORY)
    d.polygon(P([(0.86, 0.44), (0.76, 0.30), (0.70, 0.46)]), fill=IVORY)


def g_handshake(d):
    d.polygon([(S * 0.08, S * 0.62), (S * 0.44, S * 0.44), (S * 0.50, S * 0.54), (S * 0.14, S * 0.72)], fill=IVORY)
    d.polygon([(S * 0.92, S * 0.62), (S * 0.56, S * 0.44), (S * 0.50, S * 0.54), (S * 0.86, S * 0.72)], fill=IVORY)
    d.rounded_rectangle([S * 0.40, S * 0.38, S * 0.62, S * 0.60], radius=S * 0.04, fill=IVORY)
    for i in range(3):
        d.line([(S * (0.44 + i * 0.05), S * 0.38), (S * (0.44 + i * 0.05), S * 0.30)], fill=IVORY, width=int(2 * F))


def g_scales(d):
    d.line([(S * 0.50, S * 0.22), (S * 0.50, S * 0.70)], fill=IVORY, width=int(3 * F))
    d.line([(S * 0.24, S * 0.32), (S * 0.76, S * 0.32)], fill=IVORY, width=int(3 * F))
    for cx in (S * 0.26, S * 0.74):
        d.line([(cx, S * 0.32), (cx, S * 0.46)], fill=IVORY, width=int(1.8 * F))
        d.arc([cx - S * 0.10, S * 0.40, cx + S * 0.10, S * 0.58], 0, 180, fill=IVORY, width=int(2.6 * F))
    d.line([(S * 0.38, S * 0.74), (S * 0.62, S * 0.74)], fill=IVORY, width=int(3 * F))


def g_cross(d):
    d.rectangle([S * 0.44, S * 0.22, S * 0.56, S * 0.76], fill=IVORY)
    d.rectangle([S * 0.30, S * 0.38, S * 0.70, S * 0.50], fill=IVORY)


def g_laurel(d):
    d.arc([S * 0.26, S * 0.24, S * 0.74, S * 0.78], 110, 340, fill=IVORY, width=int(2.2 * F))
    for i in range(6):
        a = math.radians(300 - i * 34)
        cx, cy = S * (0.50 + math.cos(a) * 0.24), S * (0.52 + math.sin(a) * 0.27)
        d.ellipse([cx - S * 0.075, cy - S * 0.045, cx + S * 0.075, cy + S * 0.045], fill=IVORY)


def g_globe(d):
    d.ellipse([S * 0.24, S * 0.24, S * 0.76, S * 0.76], outline=IVORY, width=int(3.2 * F))
    d.arc([S * 0.36, S * 0.24, S * 0.64, S * 0.76], 0, 360, fill=IVORY, width=int(2.2 * F))
    d.line([(S * 0.24, S * 0.50), (S * 0.76, S * 0.50)], fill=IVORY, width=int(2.6 * F))
    d.arc([S * 0.24, S * 0.36, S * 0.76, S * 0.64], 0, 360, fill=IVORY, width=int(2 * F))


def g_flag(d):
    d.line([(S * 0.30, S * 0.20), (S * 0.30, S * 0.80)], fill=IVORY, width=int(3.4 * F))
    d.polygon([(S * 0.30, S * 0.24), (S * 0.76, S * 0.32), (S * 0.30, S * 0.46)], fill=IVORY)


def g_fist(d):
    d.rounded_rectangle([S * 0.36, S * 0.42, S * 0.70, S * 0.72], radius=S * 0.06, fill=IVORY)
    for i in range(3):
        x = S * (0.38 + i * 0.11)
        d.rounded_rectangle([x, S * 0.32, x + S * 0.09, S * 0.46], radius=S * 0.03, fill=IVORY)
    d.rounded_rectangle([S * 0.28, S * 0.50, S * 0.38, S * 0.66], radius=S * 0.04, fill=IVORY)
    d.rectangle([S * 0.36, S * 0.66, S * 0.70, S * 0.72], fill=(0, 0, 0, 60))


def g_flame(d):
    d.polygon([(S * 0.50, S * 0.18), (S * 0.64, S * 0.46), (S * 0.60, S * 0.70), (S * 0.50, S * 0.78),
               (S * 0.40, S * 0.70), (S * 0.36, S * 0.46)], fill=IVORY)


def g_key(d):
    d.ellipse([S * 0.24, S * 0.38, S * 0.44, S * 0.58], outline=IVORY, width=int(3.4 * F))
    d.line([(S * 0.44, S * 0.48), (S * 0.78, S * 0.48)], fill=IVORY, width=int(3.4 * F))
    d.line([(S * 0.68, S * 0.48), (S * 0.68, S * 0.60)], fill=IVORY, width=int(3 * F))
    d.line([(S * 0.76, S * 0.48), (S * 0.76, S * 0.56)], fill=IVORY, width=int(3 * F))


def g_scroll(d):
    d.rounded_rectangle([S * 0.28, S * 0.26, S * 0.72, S * 0.72], radius=S * 0.05, outline=IVORY, width=int(3.2 * F))
    for i in range(3):
        d.line([(S * 0.38, S * (0.38 + i * 0.10)), (S * 0.62, S * (0.38 + i * 0.10))], fill=IVORY, width=int(2.2 * F))


def g_bell(d):
    d.pieslice([S * 0.28, S * 0.22, S * 0.72, S * 0.66], 180, 360, fill=IVORY)
    d.polygon([(S * 0.28, S * 0.44), (S * 0.72, S * 0.44), (S * 0.84, S * 0.66), (S * 0.16, S * 0.66)], fill=IVORY)
    d.rectangle([S * 0.12, S * 0.66, S * 0.88, S * 0.72], fill=IVORY)
    d.ellipse([S * 0.44, S * 0.74, S * 0.56, S * 0.86], fill=IVORY)
    d.rectangle([S * 0.46, S * 0.14, S * 0.54, S * 0.24], fill=IVORY)


def g_bolt(d):
    d.polygon([(S * 0.56, S * 0.18), (S * 0.34, S * 0.54), (S * 0.48, S * 0.54), (S * 0.42, S * 0.80),
               (S * 0.66, S * 0.44), (S * 0.52, S * 0.44)], fill=IVORY)


def g_helmet(d):
    d.pieslice([S * 0.26, S * 0.30, S * 0.74, S * 0.78], 180, 360, fill=IVORY)
    d.rectangle([S * 0.26, S * 0.54, S * 0.74, S * 0.60], fill=IVORY)
    d.line([(S * 0.24, S * 0.60), (S * 0.76, S * 0.60)], fill=IVORY, width=int(3 * F))


import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdv_extra
GLYPHS = dict(hammer_sickle=g_hammer_sickle, cog=g_cog, star=g_star, crown=g_crown, fasces=g_fasces,
              ballot=g_ballot, tank=g_tank, plane=g_plane, ship=g_ship, anchor=g_anchor, factory=g_factory,
              wheat=g_wheat, book=g_book, radio=g_radio, torch=g_torch, sword=g_sword, shield=g_shield,
              castle=g_castle, train=g_train, derrick=g_derrick, pickaxe=g_pickaxe, handshake=g_handshake,
              scales=g_scales, cross=g_cross, laurel=g_laurel, globe=g_globe, flag=g_flag, fist=g_fist,
              flame=g_flame, key=g_key, scroll=g_scroll, bell=g_bell, bolt=g_bolt, helmet=g_helmet)
GLYPHS.update(pdv_extra.EXTRA_GLYPHS)

# keyword -> glyph, checked in order (first match wins)
KEYWORDS = [
    ('tank', 'tank'), ('armour', 'tank'), ('hull', 'tank'), ('column', 'tank'), ('combined', 'tank'),
    ('gun', 'sword'), ('batter', 'sword'), ('artillery', 'sword'), ('rifle', 'sword'), ('militia', 'sword'),
    ('soldier', 'helmet'), ('regiment', 'helmet'), ('guard', 'helmet'), ('army', 'helmet'), ('divisin', 'helmet'),
    ('fighter', 'plane'), ('intercept', 'plane'), ('air', 'plane'), ('wing', 'plane'), ('bomber', 'plane'),
    ('dive', 'plane'), ('strike', 'plane'), ('airfield', 'plane'), ('radar', 'radio'),
    ('ship', 'ship'), ('navy', 'anchor'), ('naval', 'anchor'), ('fleet', 'anchor'), ('yard', 'anchor'),
    ('marine', 'anchor'), ('convoy', 'ship'), ('cruiser', 'ship'), ('destroyer', 'ship'),
    ('submarine', 'ship'), ('pens', 'ship'), ('mine', 'ship'), ('silent', 'ship'), ('coast', 'anchor'),
    ('crown', 'crown'), ('royal', 'crown'), ('king', 'crown'), ('court', 'crown'), ('nobility', 'crown'),
    ('church', 'cross'), ('faith', 'cross'), ('oath', 'scroll'),
    ('constitution', 'scroll'), ('court', 'scales'), ('judge', 'scales'), ('settlement', 'scales'),
    ('vote', 'ballot'), ('chamber', 'ballot'), ('election', 'ballot'), ('federal', 'ballot'),
    ('press', 'book'), ('school', 'book'), ('university', 'book'), ('academy', 'book'), ('literacy', 'book'),
    ('clinic', 'cross'), ('health', 'cross'), ('hospital', 'cross'),
    ('bank', 'key'), ('budget', 'key'), ('tax', 'key'), ('treasury', 'key'), ('economy', 'key'),
    ('financ', 'key'), ('credit', 'key'),
    ('factory', 'factory'), ('plant', 'factory'), ('industry', 'factory'), ('steel', 'factory'),
    ('pits', 'pickaxe'), ('mine', 'pickaxe'), ('coal', 'pickaxe'), ('heavy', 'factory'),
    ('grain', 'wheat'), ('farm', 'wheat'), ('land', 'wheat'), ('tenant', 'wheat'), ('harvest', 'wheat'),
    ('rail', 'train'), ('railway', 'train'), ('train', 'train'), ('motorway', 'train'), ('road', 'train'),
    ('embassy', 'globe'), ('trade', 'globe'), ('diplomacy', 'globe'), ('world', 'globe'), ('league', 'globe'),
    ('neighbour', 'globe'), ('alliance', 'handshake'), ('pact', 'handshake'), ('compact', 'handshake'),
    ('party', 'fist'), ('cadre', 'fist'), ('congress', 'fist'), ('committee', 'fist'), ('commissar', 'fist'),
    ('revolution', 'fist'), ('workers', 'hammer_sickle'), ('soviet', 'hammer_sickle'), ('red', 'star'),
    ('star', 'star'), ('reich', 'fasces'), ('civil war', 'fasces'), ('fascist', 'fasces'), ('blackshirt', 'fasces'),
    ('war', 'sword'), ('fort', 'castle'), ('fortress', 'castle'), ('fortify', 'castle'),
    ('housing', 'castle'), ('city', 'castle'),
    ('radio', 'radio'), ('propaganda', 'radio'), ('news', 'radio'),
    ('oil', 'derrick'), ('fuel', 'derrick'), ('machine', 'cog'), ('plan', 'cog'), ('production', 'cog'),
    ('technology', 'bolt'), ('research', 'bolt'), ('science', 'bolt'), ('engineer', 'bolt'),
    ('security', 'shield'), ('defence', 'shield'), ('guard', 'shield'),
    ('peace', 'laurel'), ('glory', 'laurel'), ('unity', 'laurel'), ('society', 'laurel'),
    ('youth', 'flame'), ('spirit', 'flame'), ('new man', 'flame'),
    ('women', 'torch'), ('school', 'book'), ('flag', 'flag'), ('banner', 'flag'),
]

BRANCH_DEFAULT = {'cm': 'hammer_sickle', 'dm': 'ballot', 'fa': 'fasces', 'mo': 'crown',
                  'af': 'helmet', 'nv': 'anchor'}


def glyph_for(fid, name):
    if fid in pdv_extra.ICON_BY_ID:
        return pdv_extra.ICON_BY_ID[fid]
    low = name.lower()
    for kw, gl in KEYWORDS:
        if kw in low:
            return gl
    key = fid.split('_')[1]
    return BRANCH_DEFAULT.get(key, 'star')


def make_icon(path, glyph, pal, shape):
    img = plate(shape, pal)
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    GLYPHS[glyph](d)
    gs = int(S * 0.97)
    lay = lay.resize((gs, gs), Image.LANCZOS)
    tmp = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    tmp.paste(lay, ((S - gs) // 2, (S - gs) // 2), lay)
    lay = tmp
    # soft shadow
    sh = lay.filter(__import__('PIL.ImageFilter', fromlist=['Filter']).GaussianBlur(4))
    shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 140), (0, int(1.2 * F)), sh)
    img = Image.alpha_composite(img, shadow)
    img = Image.alpha_composite(img, lay)
    img = img.resize((68, 68), Image.LANCZOS)
    png = '/home/user/pdv_png/' + os.path.basename(path).replace('.dds', '.png')
    os.makedirs(os.path.dirname(png), exist_ok=True)
    img.save(png)
    return png


def write_dds(png, dds):
    subprocess.run(['convert', png, '-define', 'dds:compression=dxt5', '-define', 'dds:mipmaps=0', dds],
                   check=True)


GFX_HEAD = 'spriteTypes = {\n'


def write_gfx(sprites):
    lines = [GFX_HEAD]
    for name, tex in sprites:
        lines.append('\tSpriteType = {\n\t\tname = "%s"\n\t\ttexturefile = "%s"\n\t}\n' % (name, tex))
    lines.append('}\n')
    path = MOD + 'Interface/pdv_vyratia_goals.gfx'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8', newline='\n').write(''.join(lines))
    return path


def rewrite_tree(sprites):
    """Point every generated focus at its own sprite; leave the six vanilla ones alone."""
    tree = MOD + 'common/national_focus/PDV_vyratia.txt'
    s = open(tree, encoding='utf-8-sig').read()
    names = {n.replace('GFX_', ''): n for n, _ in sprites}

    def fix(m):
        block = m.group(0)
        fid = re.search(r'id = (\S+)', block).group(1)
        sprite = names.get(fid.lower())
        if not sprite:
            return block
        return re.sub(r'icon = \S+', 'icon = ' + sprite, block, count=1)

    out = re.sub(r'\tfocus = \{[\s\S]*?\n\t\}', fix, s)
    open(tree, 'w', encoding='utf-8', newline='\n').write(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    tree = MOD + 'common/national_focus/PDV_vyratia.txt'
    src = open(tree, encoding='utf-8-sig').read()
    loc = open(MOD + 'Localisation/English/replace/pdv_vyratia_l_english.yml', encoding='utf-8-sig').read()
    names = dict(re.findall(r' (\w+):0 "([^"]*)"', loc))

    KEEP_VANILLA = {'PDV_the_directorate', 'PDV_four_roads', 'PDV_cm_review', 'PDV_dm_review',
                    'PDV_fa_review', 'PDV_mo_review'}
    sprites = []
    pngs = []
    for m in re.finditer(r'\tfocus = \{[\s\S]*?\n\t\}', src):
        b = m.group(0)
        fid = re.search(r'id = (\S+)', b).group(1)
        if fid in KEEP_VANILLA:
            continue
        branch = fid.split('_')[1]
        pal = PALETTE.get(branch, PALETTE['cm'])
        gl = glyph_for(fid, names.get(fid, fid))
        shape = {'cm': 'circle', 'dm': 'circle', 'fa': 'shield', 'mo': 'shield',
                 'af': 'shield', 'nv': 'diamond'}.get(branch, 'circle')
        png = make_icon(OUT + fid.lower() + '.dds', gl, pal, shape)
        write_dds(png, png.replace('.png', '.dds'))
        pngs.append(png)
        sprites.append(('GFX_' + fid.lower(), 'gfx/interface/goals/pdv/' + fid.lower() + '.dds'))
    write_gfx(sprites)
    rewrite_tree(sprites)
    print('icons', len(sprites))
    return sprites, pngs


if __name__ == '__main__':
    main()
