# -*- coding: utf-8 -*-
"""Extra vector glyphs + explicit per-focus icon map for the Vyratia focus tree."""
import math
from PIL import ImageDraw

S = 272
F = 4.0
IVORY = (243, 233, 202, 255)


def R(a, b, c, d):
    return [S * a, S * b, S * c, S * d]


def P(pts):
    return [(S * x, S * y) for x, y in pts]


def W(mult=1.0):
    return max(1, int(4.6 * F * mult))


def g_anvil(d):
    d.polygon(P([(0.18, 0.34), (0.80, 0.34), (0.70, 0.46), (0.56, 0.52), (0.56, 0.62),
                 (0.68, 0.70), (0.32, 0.70), (0.44, 0.62), (0.44, 0.52)]), fill=IVORY)
    d.polygon(P([(0.80, 0.34), (0.82, 0.28), (0.62, 0.28), (0.62, 0.34)]), fill=IVORY)
    d.rectangle(R(0.30, 0.70, 0.70, 0.76), fill=IVORY)


def g_blocks(d):
    for i in range(2):
        for j in range(2):
            x = 0.22 + i * 0.30
            y = 0.24 + j * 0.30
            d.rectangle(R(x, y, x + 0.26, y + 0.26), outline=IVORY, width=W(0.85))
    d.rectangle(R(0.18, 0.80, 0.82, 0.84), fill=IVORY)


def g_bread(d):
    d.pieslice(R(0.20, 0.32, 0.80, 0.78), 180, 360, fill=IVORY)
    d.rectangle(R(0.20, 0.55, 0.80, 0.74), fill=IVORY)
    d.line([(S * 0.32, S * 0.52), (S * 0.38, S * 0.36)], fill=(0, 0, 0, 90), width=W(0.6))
    d.line([(S * 0.50, S * 0.52), (S * 0.52, S * 0.36)], fill=(0, 0, 0, 90), width=W(0.6))
    d.line([(S * 0.68, S * 0.52), (S * 0.66, S * 0.36)], fill=(0, 0, 0, 90), width=W(0.6))


def g_rifle(d):
    d.line([(S * 0.18, S * 0.74), (S * 0.80, S * 0.26)], fill=IVORY, width=W(0.9))
    d.line([(S * 0.70, S * 0.34), (S * 0.84, S * 0.44)], fill=IVORY, width=W(0.9))
    d.polygon(P([(0.14, 0.78), (0.30, 0.72), (0.24, 0.62)]), fill=IVORY)
    d.line([(S * 0.38, S * 0.56), (S * 0.46, S * 0.64)], fill=IVORY, width=W(0.7))


def g_library(d):
    for x, y, w in ((0.18, 0.56, 0.62), (0.22, 0.38, 0.56), (0.26, 0.20, 0.46)):
        d.rounded_rectangle(R(x, y, x + w, y + 0.14), radius=S * 0.02, fill=IVORY)
        d.rectangle(R(x, y + 0.10, x + w, y + 0.14), fill=(0, 0, 0, 90))
    d.line([(S * 0.84, S * 0.20), (S * 0.78, S * 0.70)], fill=IVORY, width=W(0.6))


def g_tools(d):
    d.line([(S * 0.26, S * 0.76), (S * 0.66, S * 0.34)], fill=IVORY, width=W(0.85))
    d.line([(S * 0.34, S * 0.34), (S * 0.72, S * 0.76)], fill=IVORY, width=W(0.85))
    d.ellipse(R(0.60, 0.20, 0.80, 0.40), outline=IVORY, width=W(0.7))
    d.rectangle(R(0.26, 0.62, 0.44, 0.78), fill=IVORY)


def g_map(d):
    d.polygon(P([(0.16, 0.30), (0.38, 0.24), (0.62, 0.32), (0.84, 0.24), (0.84, 0.72),
                 (0.62, 0.80), (0.38, 0.72), (0.16, 0.78)]), outline=IVORY, width=W(0.8))
    d.line([(S * 0.38, S * 0.24), (S * 0.38, S * 0.72)], fill=IVORY, width=W(0.6))
    d.line([(S * 0.62, S * 0.32), (S * 0.62, S * 0.80)], fill=IVORY, width=W(0.6))
    d.line([(S * 0.22, S * 0.56), (S * 0.34, S * 0.50)], fill=IVORY, width=W(0.5))


def g_mountains(d):
    d.polygon(P([(0.10, 0.74), (0.38, 0.28), (0.62, 0.74)]), fill=IVORY)
    d.polygon(P([(0.44, 0.74), (0.70, 0.38), (0.92, 0.74)]), fill=IVORY)
    d.polygon(P([(0.30, 0.46), (0.38, 0.28), (0.46, 0.46)]), fill=(0, 0, 0, 70))
    d.line([(S * 0.08, S * 0.78), (S * 0.92, S * 0.78)], fill=IVORY, width=W(0.6))


def g_hand(d):
    d.rounded_rectangle(R(0.30, 0.40, 0.70, 0.78), radius=S * 0.06, fill=IVORY)
    for i in range(4):
        x = 0.31 + i * 0.10
        d.rounded_rectangle(R(x, 0.22 + abs(i - 1.5) * 0.03, x + 0.08, 0.46), radius=S * 0.03, fill=IVORY)
    d.rounded_rectangle(R(0.20, 0.46, 0.32, 0.66), radius=S * 0.05, fill=IVORY)


def g_crate(d):
    d.rectangle(R(0.20, 0.26, 0.80, 0.74), outline=IVORY, width=W(0.85))
    d.line([(S * 0.20, S * 0.26), (S * 0.80, S * 0.74)], fill=IVORY, width=W(0.55))
    d.line([(S * 0.80, S * 0.26), (S * 0.20, S * 0.74)], fill=IVORY, width=W(0.55))
    d.rectangle(R(0.20, 0.44, 0.80, 0.56), fill=IVORY)


def g_dove(d):
    d.ellipse(R(0.30, 0.40, 0.70, 0.58), fill=IVORY)
    d.ellipse(R(0.64, 0.30, 0.78, 0.44), fill=IVORY)
    d.polygon(P([(0.76, 0.36), (0.90, 0.38), (0.76, 0.42)]), fill=IVORY)
    d.polygon(P([(0.18, 0.44), (0.34, 0.46), (0.28, 0.60)]), fill=IVORY)
    d.polygon(P([(0.34, 0.42), (0.58, 0.20), (0.64, 0.40)]), fill=IVORY)
    d.line([(S * 0.50, S * 0.58), (S * 0.44, S * 0.70)], fill=IVORY, width=W(0.5))
    d.line([(S * 0.58, S * 0.58), (S * 0.54, S * 0.70)], fill=IVORY, width=W(0.5))


def g_columns(d):
    d.polygon(P([(0.12, 0.30), (0.50, 0.16), (0.88, 0.30)]), fill=IVORY)
    for x in (0.20, 0.42, 0.64):
        d.rectangle(R(x, 0.36, x + 0.16, 0.70), fill=IVORY)
    d.rectangle(R(0.14, 0.70, 0.86, 0.78), fill=IVORY)
    d.rectangle(R(0.14, 0.24, 0.86, 0.29), fill=IVORY)


def g_island(d):
    d.pieslice(R(0.24, 0.34, 0.76, 0.70), 180, 360, fill=IVORY)
    d.rectangle(R(0.24, 0.50, 0.76, 0.54), fill=IVORY)
    for i in range(3):
        d.line([(S * (0.12 + i * 0.02), S * (0.66 + i * 0.09)), (S * (0.88 - i * 0.02), S * (0.66 + i * 0.09))],
               fill=IVORY, width=W(0.45))


def g_envelope(d):
    d.rectangle(R(0.16, 0.32, 0.84, 0.68), outline=IVORY, width=W(0.85))
    d.line([(S * 0.16, S * 0.32), (S * 0.50, S * 0.56), (S * 0.84, S * 0.32)], fill=IVORY,
           width=W(0.7), joint='curve')


def g_gavel(d):
    d.line([(S * 0.22, S * 0.30), (S * 0.70, S * 0.64)], fill=IVORY, width=W(0.8))
    d.polygon(P([(0.60, 0.16), (0.84, 0.34), (0.70, 0.50), (0.46, 0.32)]), fill=IVORY)
    d.rectangle(R(0.16, 0.72, 0.84, 0.80), fill=IVORY)


def g_heart(d):
    d.ellipse(R(0.22, 0.28, 0.50, 0.56), fill=IVORY)
    d.ellipse(R(0.50, 0.28, 0.78, 0.56), fill=IVORY)
    d.polygon(P([(0.22, 0.48), (0.78, 0.48), (0.50, 0.80)]), fill=IVORY)


def g_road(d):
    d.polygon(P([(0.40, 0.22), (0.60, 0.22), (0.88, 0.80), (0.12, 0.80)]), outline=IVORY, width=W(0.8))
    for y, h in ((0.32, 0.06), (0.46, 0.08), (0.62, 0.10)):
        d.rectangle(R(0.48, y, 0.52, y + h), fill=IVORY)


def g_truck(d):
    d.rectangle(R(0.16, 0.36, 0.60, 0.62), fill=IVORY)
    d.polygon(P([(0.60, 0.44), (0.80, 0.44), (0.86, 0.56), (0.86, 0.62), (0.60, 0.62)]), fill=IVORY)
    for x in (0.28, 0.44, 0.74):
        d.ellipse(R(x - 0.07, 0.60, x + 0.07, 0.74), fill=(0, 0, 0, 160))
        d.ellipse(R(x - 0.07, 0.60, x + 0.07, 0.74), outline=IVORY, width=W(0.5))


def g_bomb(d):
    d.ellipse(R(0.28, 0.36, 0.60, 0.80), fill=IVORY)
    d.polygon(P([(0.46, 0.40), (0.40, 0.22), (0.50, 0.30), (0.56, 0.16), (0.60, 0.38)]), fill=IVORY)
    d.line([(S * 0.60, S * 0.34), (S * 0.74, S * 0.24)], fill=IVORY, width=W(0.45))
    d.ellipse(R(0.74, 0.18, 0.84, 0.28), fill=IVORY)


def g_runway(d):
    d.polygon(P([(0.34, 0.16), (0.66, 0.16), (0.88, 0.80), (0.12, 0.80)]), fill=IVORY)
    d.polygon(P([(0.44, 0.24), (0.56, 0.24), (0.60, 0.72), (0.40, 0.72)]), fill=(0, 0, 0, 120))


def g_sub(d):
    d.ellipse(R(0.14, 0.42, 0.86, 0.68), fill=IVORY)
    d.rectangle(R(0.42, 0.28, 0.58, 0.46), fill=IVORY)
    d.line([(S * 0.50, S * 0.28), (S * 0.56, S * 0.18)], fill=IVORY, width=W(0.5))
    d.line([(S * 0.14, S * 0.74), (S * 0.86, S * 0.74)], fill=IVORY, width=W(0.45))


def g_periscope(d):
    d.rectangle(R(0.42, 0.30, 0.54, 0.76), fill=IVORY)
    d.line([(S * 0.48, S * 0.34), (S * 0.70, S * 0.26)], fill=IVORY, width=W(0.7))
    d.rectangle(R(0.66, 0.16, 0.82, 0.30), fill=IVORY)
    d.line([(S * 0.24, S * 0.56), (S * 0.36, S * 0.56)], fill=IVORY, width=W(0.45))
    d.line([(S * 0.24, S * 0.66), (S * 0.36, S * 0.66)], fill=IVORY, width=W(0.45))


def g_battleship(d):
    d.polygon(P([(0.10, 0.50), (0.90, 0.50), (0.80, 0.68), (0.20, 0.68)]), fill=IVORY)
    d.rectangle(R(0.40, 0.34, 0.62, 0.50), fill=IVORY)
    for x in (0.28, 0.72):
        d.rectangle(R(x - 0.06, 0.38, x + 0.06, 0.50), fill=IVORY)
        d.line([(S * x, S * 0.38), (S * (x + 0.10), S * 0.28)], fill=IVORY, width=W(0.4))
    d.line([(S * 0.10, S * 0.74), (S * 0.90, S * 0.74)], fill=IVORY, width=W(0.45))


def g_fleet(d):
    for x, y, w in ((0.14, 0.28, 0.34), (0.52, 0.30, 0.34), (0.32, 0.56, 0.36)):
        d.polygon(P([(x, y), (x + w, y), (x + w - 0.06, y + 0.14), (x + 0.06, y + 0.14)]), fill=IVORY)
        d.rectangle(R(x + w / 2 - 0.03, y - 0.09, x + w / 2 + 0.03, y), fill=IVORY)


def g_mine(d):
    d.ellipse(R(0.32, 0.32, 0.68, 0.68), fill=IVORY)
    for i in range(8):
        a = i * math.pi / 4
        d.line([(S * 0.50, S * 0.50),
                (S * (0.50 + math.cos(a) * 0.30), S * (0.50 + math.sin(a) * 0.30))], fill=IVORY, width=W(0.5))


def g_crane(d):
    d.line([(S * 0.36, S * 0.20), (S * 0.36, S * 0.82)], fill=IVORY, width=W(0.8))
    d.line([(S * 0.20, S * 0.24), (S * 0.82, S * 0.24)], fill=IVORY, width=W(0.8))
    d.line([(S * 0.36, S * 0.20), (S * 0.20, S * 0.46)], fill=IVORY, width=W(0.4))
    d.line([(S * 0.74, S * 0.24), (S * 0.74, S * 0.46)], fill=IVORY, width=W(0.45))
    d.rectangle(R(0.66, 0.46, 0.82, 0.56), fill=IVORY)
    d.rectangle(R(0.20, 0.82, 0.52, 0.88), fill=IVORY)


def g_target(d):
    d.ellipse(R(0.20, 0.20, 0.80, 0.80), outline=IVORY, width=W(0.85))
    d.ellipse(R(0.36, 0.36, 0.64, 0.64), outline=IVORY, width=W(0.7))
    d.ellipse(R(0.46, 0.46, 0.54, 0.54), fill=IVORY)


def g_shell(d):
    d.polygon(P([(0.36, 0.62), (0.64, 0.62), (0.64, 0.30), (0.50, 0.18), (0.36, 0.30)]), fill=IVORY)
    d.rectangle(R(0.34, 0.62, 0.66, 0.76), fill=IVORY)
    d.line([(S * 0.30, S * 0.80), (S * 0.70, S * 0.80)], fill=IVORY, width=W(0.45))


def g_eye(d):
    d.polygon(P([(0.10, 0.50), (0.50, 0.26), (0.90, 0.50), (0.50, 0.74)]), outline=IVORY, width=W(0.7))
    d.ellipse(R(0.40, 0.40, 0.60, 0.60), fill=IVORY)


def g_megaphone(d):
    d.polygon(P([(0.20, 0.40), (0.60, 0.24), (0.60, 0.76), (0.20, 0.60)]), fill=IVORY)
    d.rectangle(R(0.10, 0.42, 0.22, 0.58), fill=IVORY)
    d.line([(S * 0.70, S * 0.32), (S * 0.84, S * 0.26)], fill=IVORY, width=W(0.5))
    d.line([(S * 0.70, S * 0.68), (S * 0.84, S * 0.74)], fill=IVORY, width=W(0.5))


def g_newspaper(d):
    d.rectangle(R(0.16, 0.28, 0.84, 0.74), outline=IVORY, width=W(0.8))
    d.rectangle(R(0.24, 0.34, 0.76, 0.42), fill=IVORY)
    for i in range(3):
        y = 0.50 + i * 0.08
        d.line([(S * 0.24, S * y), (S * 0.76, S * y)], fill=IVORY, width=W(0.4))


def g_chains(d):
    d.ellipse(R(0.12, 0.26, 0.54, 0.54), outline=IVORY, width=W(0.75))
    d.ellipse(R(0.46, 0.44, 0.88, 0.72), outline=IVORY, width=W(0.75))


def g_eagle(d):
    d.polygon(P([(0.50, 0.46), (0.30, 0.30), (0.08, 0.34), (0.26, 0.44), (0.10, 0.50),
                 (0.32, 0.54), (0.44, 0.60), (0.50, 0.72), (0.56, 0.60), (0.68, 0.54),
                 (0.90, 0.50), (0.74, 0.44), (0.92, 0.34), (0.70, 0.30)]), fill=IVORY)
    d.ellipse(R(0.44, 0.20, 0.58, 0.34), fill=IVORY)
    d.polygon(P([(0.56, 0.26), (0.70, 0.28), (0.56, 0.32)]), fill=IVORY)


def g_sun(d):
    d.ellipse(R(0.34, 0.34, 0.66, 0.66), fill=IVORY)
    for i in range(8):
        a = i * math.pi / 4
        d.line([(S * (0.50 + math.cos(a) * 0.18), S * (0.50 + math.sin(a) * 0.18)),
                (S * (0.50 + math.cos(a) * 0.32), S * (0.50 + math.sin(a) * 0.32))], fill=IVORY, width=W(0.55))


def g_quill(d):
    d.polygon(P([(0.74, 0.18), (0.80, 0.40), (0.44, 0.72), (0.30, 0.80), (0.34, 0.62)]), fill=IVORY)
    d.line([(S * 0.30, S * 0.82), (S * 0.62, S * 0.50)], fill=IVORY, width=W(0.45))
    d.line([(S * 0.44, S * 0.56), (S * 0.60, S * 0.62)], fill=(0, 0, 0, 90), width=W(0.35))


def g_coin(d):
    d.ellipse(R(0.20, 0.20, 0.80, 0.80), fill=IVORY)
    d.ellipse(R(0.30, 0.30, 0.70, 0.70), outline=(0, 0, 0, 120), width=W(0.5))
    d.line([(S * 0.50, S * 0.36), (S * 0.50, S * 0.64)], fill=(0, 0, 0, 120), width=W(0.45))
    d.line([(S * 0.40, S * 0.44), (S * 0.60, S * 0.44)], fill=(0, 0, 0, 120), width=W(0.4))


def g_plough(d):
    d.line([(S * 0.16, S * 0.34), (S * 0.60, S * 0.64)], fill=IVORY, width=W(0.8))
    d.polygon(P([(0.52, 0.56), (0.84, 0.60), (0.74, 0.80), (0.46, 0.74)]), fill=IVORY)
    d.ellipse(R(0.08, 0.26, 0.26, 0.44), outline=IVORY, width=W(0.5))
    d.line([(S * 0.62, S * 0.60), (S * 0.80, S * 0.34)], fill=IVORY, width=W(0.5))


def g_bridge(d):
    d.arc(R(0.14, 0.30, 0.86, 0.86), 180, 360, fill=IVORY, width=W(1.0))
    d.rectangle(R(0.10, 0.54, 0.90, 0.60), fill=IVORY)
    for x in (0.28, 0.50, 0.72):
        d.line([(S * x, S * 0.60), (S * x, S * 0.78)], fill=IVORY, width=W(0.45))


def g_throne(d):
    d.rounded_rectangle(R(0.34, 0.12, 0.66, 0.56), radius=S * 0.04, fill=IVORY)
    d.rectangle(R(0.24, 0.52, 0.76, 0.60), fill=IVORY)
    d.rectangle(R(0.18, 0.38, 0.28, 0.60), fill=IVORY)
    d.rectangle(R(0.72, 0.38, 0.82, 0.60), fill=IVORY)
    d.rectangle(R(0.28, 0.60, 0.38, 0.84), fill=IVORY)
    d.rectangle(R(0.62, 0.60, 0.72, 0.84), fill=IVORY)
    d.polygon(P([(0.34, 0.12), (0.40, 0.02), (0.50, 0.10), (0.60, 0.02), (0.66, 0.12)]), fill=IVORY)


def g_sceptre(d):
    d.line([(S * 0.42, S * 0.84), (S * 0.56, S * 0.34)], fill=IVORY, width=W(0.9))
    d.ellipse(R(0.46, 0.14, 0.72, 0.40), fill=IVORY)
    d.line([(S * 0.59, S * 0.10), (S * 0.59, S * 0.18)], fill=IVORY, width=W(0.4))


def g_compass(d):
    d.ellipse(R(0.18, 0.18, 0.82, 0.82), outline=IVORY, width=W(0.85))
    d.polygon(P([(0.50, 0.26), (0.60, 0.52), (0.50, 0.74), (0.40, 0.52)]), fill=IVORY)


def g_binoculars(d):
    for x in (0.18, 0.52):
        d.rounded_rectangle(R(x, 0.24, x + 0.30, 0.76), radius=S * 0.07, fill=IVORY)
        d.ellipse(R(x + 0.06, 0.62, x + 0.24, 0.80), fill=(0, 0, 0, 130))
    d.rectangle(R(0.44, 0.40, 0.56, 0.52), fill=IVORY)


def g_hammer(d):
    d.line([(S * 0.30, S * 0.80), (S * 0.62, S * 0.36)], fill=IVORY, width=W(0.85))
    d.polygon(P([(0.52, 0.14), (0.80, 0.28), (0.70, 0.46), (0.42, 0.32)]), fill=IVORY)


def g_sickle(d):
    d.arc(R(0.22, 0.26, 0.78, 0.82), 200, 20, fill=IVORY, width=W(0.95))
    d.line([(S * 0.72, S * 0.30), (S * 0.62, S * 0.40)], fill=IVORY, width=W(0.95))


def g_cavalry(d):
    d.polygon(P([(0.30, 0.82), (0.32, 0.52), (0.38, 0.30), (0.50, 0.20), (0.64, 0.24),
                 (0.74, 0.34), (0.86, 0.40), (0.70, 0.44), (0.68, 0.52), (0.76, 0.64),
                 (0.46, 0.66), (0.46, 0.82)]), fill=IVORY)
    d.polygon(P([(0.52, 0.20), (0.54, 0.08), (0.62, 0.20)]), fill=IVORY)
    d.rectangle(R(0.24, 0.82, 0.54, 0.88), fill=IVORY)


def g_radar(d):
    d.arc(R(0.20, 0.26, 0.80, 0.74), 200, 340, fill=IVORY, width=W(0.9))
    d.line([(S * 0.50, S * 0.56), (S * 0.50, S * 0.80)], fill=IVORY, width=W(0.5))
    d.rectangle(R(0.34, 0.80, 0.66, 0.86), fill=IVORY)
    d.line([(S * 0.56, S * 0.44), (S * 0.78, S * 0.26)], fill=IVORY, width=W(0.4))


EXTRA_GLYPHS = dict(cavalry=g_cavalry, radar=g_radar, anvil=g_anvil, blocks=g_blocks, bread=g_bread, rifle=g_rifle, library=g_library,
                    tools=g_tools, map=g_map, mountains=g_mountains, hand=g_hand, crate=g_crate,
                    dove=g_dove, columns=g_columns, island=g_island, envelope=g_envelope, gavel=g_gavel,
                    heart=g_heart, road=g_road, truck=g_truck, bomb=g_bomb, runway=g_runway,
                    sub=g_sub, periscope=g_periscope, battleship=g_battleship, fleet=g_fleet,
                    mine=g_mine, crane=g_crane, target=g_target, shell=g_shell, eye=g_eye,
                    megaphone=g_megaphone, newspaper=g_newspaper, chains=g_chains, eagle=g_eagle,
                    sun=g_sun, quill=g_quill, coin=g_coin, plough=g_plough, bridge=g_bridge,
                    throne=g_throne, sceptre=g_sceptre, compass=g_compass, binoculars=g_binoculars,
                    hammer=g_hammer, sickle=g_sickle)

# explicit glyph per focus (overrides the keyword guess)
ICON_BY_ID = {
    # ---- communist
    'PDV_cm_c0_0': 'pickaxe', 'PDV_cm_c0_1': 'cog', 'PDV_cm_c0_2': 'factory', 'PDV_cm_c0_3': 'wheat',
    'PDV_cm_c0_4': 'coin', 'PDV_cm_c0_5': 'train', 'PDV_cm_c0_6': 'anvil', 'PDV_cm_c0_7': 'hammer',
    'PDV_cm_c1_0': 'book', 'PDV_cm_c1_1': 'blocks', 'PDV_cm_c1_2': 'cross', 'PDV_cm_c1_3': 'torch',
    'PDV_cm_c1_4': 'scroll', 'PDV_cm_c1_5': 'newspaper', 'PDV_cm_c1_6': 'bread', 'PDV_cm_c1_7': 'handshake',
    'PDV_cm_c2_0': 'rifle', 'PDV_cm_c2_1': 'tank', 'PDV_cm_c2_2': 'shell', 'PDV_cm_c2_3': 'star',
    'PDV_cm_c2_4': 'megaphone', 'PDV_cm_c2_5': 'castle', 'PDV_cm_c2_6': 'radio', 'PDV_cm_c2_7': 'fist',
    'PDV_cm_c3_0': 'globe', 'PDV_cm_c3_1': 'hammer_sickle', 'PDV_cm_c3_2': 'map', 'PDV_cm_c3_3': 'flag',
    'PDV_cm_c3_4': 'hand', 'PDV_cm_c3_5': 'quill', 'PDV_cm_c3_6': 'mountains', 'PDV_cm_c3_7': 'flame',
    'PDV_cm_spine1': 'helmet', 'PDV_cm_spine2': 'library', 'PDV_cm_spine3': 'tools', 'PDV_cm_spine4': 'sword',
    'PDV_cm_spine5': 'shield', 'PDV_cm_spine6': 'sickle', 'PDV_cm_final': 'sickle',
    # ---- democratic
    'PDV_dm_c0_0': 'newspaper', 'PDV_dm_c0_1': 'scales', 'PDV_dm_c0_2': 'coin', 'PDV_dm_c0_3': 'plough',
    'PDV_dm_c0_4': 'handshake', 'PDV_dm_c0_5': 'scroll', 'PDV_dm_c0_6': 'bridge', 'PDV_dm_c0_7': 'ship',
    'PDV_dm_c1_0': 'book', 'PDV_dm_c1_1': 'cross', 'PDV_dm_c1_2': 'blocks', 'PDV_dm_c1_3': 'ballot',
    'PDV_dm_c1_4': 'hand', 'PDV_dm_c1_5': 'laurel', 'PDV_dm_c1_6': 'library', 'PDV_dm_c1_7': 'sun',
    'PDV_dm_c2_0': 'dove', 'PDV_dm_c2_1': 'shield', 'PDV_dm_c2_2': 'quill', 'PDV_dm_c2_3': 'map',
    'PDV_dm_c2_4': 'columns', 'PDV_dm_c2_5': 'plane', 'PDV_dm_c2_6': 'binoculars', 'PDV_dm_c2_7': 'rifle',
    'PDV_dm_c3_0': 'globe', 'PDV_dm_c3_1': 'crate', 'PDV_dm_c3_2': 'island', 'PDV_dm_c3_3': 'gavel',
    'PDV_dm_c3_4': 'envelope', 'PDV_dm_c3_5': 'chains', 'PDV_dm_c3_6': 'dove', 'PDV_dm_c3_7': 'star',
    'PDV_dm_spine1': 'eye', 'PDV_dm_spine2': 'columns', 'PDV_dm_spine3': 'helmet', 'PDV_dm_spine4': 'scroll',
    'PDV_dm_spine5': 'gavel', 'PDV_dm_spine6': 'flag', 'PDV_dm_final': 'laurel',
    # ---- fascist
    'PDV_fa_c0_0': 'cog', 'PDV_fa_c0_1': 'coin', 'PDV_fa_c0_2': 'factory', 'PDV_fa_c0_3': 'wheat',
    'PDV_fa_c0_4': 'key', 'PDV_fa_c0_5': 'road', 'PDV_fa_c0_6': 'anvil', 'PDV_fa_c0_7': 'derrick',
    'PDV_fa_c1_0': 'flame', 'PDV_fa_c1_1': 'book', 'PDV_fa_c1_2': 'megaphone', 'PDV_fa_c1_3': 'heart',
    'PDV_fa_c1_4': 'tools', 'PDV_fa_c1_5': 'plough', 'PDV_fa_c1_6': 'torch', 'PDV_fa_c1_7': 'laurel',
    'PDV_fa_c2_0': 'rifle', 'PDV_fa_c2_1': 'tank', 'PDV_fa_c2_2': 'plane', 'PDV_fa_c2_3': 'sword',
    'PDV_fa_c2_4': 'castle', 'PDV_fa_c2_5': 'shield', 'PDV_fa_c2_6': 'helmet', 'PDV_fa_c2_7': 'shell',
    'PDV_fa_c3_0': 'map', 'PDV_fa_c3_1': 'globe', 'PDV_fa_c3_2': 'cross', 'PDV_fa_c3_3': 'fasces',
    'PDV_fa_c3_4': 'eye', 'PDV_fa_c3_5': 'chains', 'PDV_fa_c3_6': 'mountains', 'PDV_fa_c3_7': 'eagle',
    'PDV_fa_spine1': 'helmet', 'PDV_fa_spine2': 'library', 'PDV_fa_spine3': 'bolt', 'PDV_fa_spine4': 'fist',
    'PDV_fa_spine5': 'sun', 'PDV_fa_spine6': 'flag', 'PDV_fa_final': 'eagle',
    # ---- monarchist
    'PDV_mo_c0_0': 'castle', 'PDV_mo_c0_1': 'coin', 'PDV_mo_c0_2': 'wheat', 'PDV_mo_c0_3': 'laurel',
    'PDV_mo_c0_4': 'road', 'PDV_mo_c0_5': 'coin', 'PDV_mo_c0_6': 'quill', 'PDV_mo_c0_7': 'dove',
    'PDV_mo_c1_0': 'cross', 'PDV_mo_c1_1': 'heart', 'PDV_mo_c1_2': 'bread', 'PDV_mo_c1_3': 'scales',
    'PDV_mo_c1_4': 'flag', 'PDV_mo_c1_5': 'library', 'PDV_mo_c1_6': 'torch', 'PDV_mo_c1_7': 'crown',
    'PDV_mo_c2_0': 'helmet', 'PDV_mo_c2_1': 'cavalry', 'PDV_mo_c2_2': 'castle', 'PDV_mo_c2_3': 'anchor',
    'PDV_mo_c2_4': 'sceptre', 'PDV_mo_c2_5': 'tools', 'PDV_mo_c2_6': 'helmet', 'PDV_mo_c2_7': 'crown',
    'PDV_mo_c3_0': 'throne', 'PDV_mo_c3_1': 'envelope', 'PDV_mo_c3_2': 'map', 'PDV_mo_c3_3': 'crown',
    'PDV_mo_c3_4': 'handshake', 'PDV_mo_c3_5': 'flag', 'PDV_mo_c3_6': 'quill', 'PDV_mo_c3_7': 'sceptre',
    'PDV_mo_spine1': 'helmet', 'PDV_mo_spine2': 'scroll', 'PDV_mo_spine3': 'anvil', 'PDV_mo_spine4': 'sword',
    'PDV_mo_spine5': 'cavalry', 'PDV_mo_spine6': 'crown', 'PDV_mo_final': 'throne',
    # ---- army / air
    'PDV_af_root': 'helmet', 'PDV_af_armour': 'tank', 'PDV_af_guns': 'target', 'PDV_af_hulls': 'cog',
    'PDV_af_barrels': 'factory', 'PDV_af_columns': 'truck', 'PDV_af_battery': 'shell',
    'PDV_af_combined': 'sword', 'PDV_af_counterbattery': 'binoculars', 'PDV_af_manual': 'book',
    'PDV_af_air': 'plane', 'PDV_af_fighters': 'bolt', 'PDV_af_cas': 'bomb', 'PDV_af_radar': 'radar',
    'PDV_af_airfields': 'runway', 'PDV_af_strike': 'plane', 'PDV_af_wing': 'plane',
    'PDV_af_divebomber': 'bomb', 'PDV_af_airdoctrine': 'map', 'PDV_af_capstone': 'eagle',
    # ---- navy
    'PDV_nv_root': 'crane', 'PDV_nv_surface': 'ship', 'PDV_nv_subs': 'sub', 'PDV_nv_cruisers': 'battleship',
    'PDV_nv_pens': 'castle', 'PDV_nv_destroyers': 'fleet', 'PDV_nv_wolfpack': 'sub',
    'PDV_nv_battleline': 'battleship', 'PDV_nv_mines': 'mine', 'PDV_nv_screen': 'shield',
    'PDV_nv_silent': 'periscope', 'PDV_nv_doctrine': 'map', 'PDV_nv_coast': 'castle',
    'PDV_nv_marines': 'rifle', 'PDV_nv_convoys': 'crate', 'PDV_nv_tradewar': 'chains',
    'PDV_nv_admiralty': 'anchor', 'PDV_nv_academy': 'compass', 'PDV_nv_fleetair': 'plane',
    'PDV_nv_law': 'scroll',
}
