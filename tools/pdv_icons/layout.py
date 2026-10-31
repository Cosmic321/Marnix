# -*- coding: utf-8 -*-
"""Geometry and prerequisites for the Vyratia focus tree.

Shape (after the Soviet tree): the four roads stand side by side at the top.
Each road is a lattice - a row of four focuses, then a hub that requires all
four of them, then the next row of four. You cannot walk down the middle and
ignore the sides, because the middle *is* the sides.
"""
import random
import re

MOD = '/home/user/Marnix/CosmicDaWinner/'
TREE = MOD + 'common/national_focus/PDV_vyratia.txt'
LOC = MOD + 'Localisation/English/replace/pdv_vyratia_l_english.yml'

BAND = {'cm': 0, 'dm': 9, 'fa': 17, 'mo': 25}   # uneven gaps on purpose
COLS = {'c0': 0, 'c1': 2, 'c2': 4, 'c3': 6}     # the four focuses in a row
HUB = 3                                          # hub sits in the middle

TRUNK = {'PDV_the_directorate': (15, 0), 'PDV_four_roads': (15, 1)}

# rows of four, and the hubs that demand all four. Nothing here is a fixed
# rhythm: each road rolls its own row shapes and spacing, so the four roads
# read as hand-built branches rather than four copies of one lattice.
HUB_ROWS = {0: 'spine2', 2: 'spine3', 4: 'spine4', 6: 'spine5', 7: 'spine6'}

# where a row's four focuses can stand inside its seven-column band
ROW_SHAPES = [(0, 1, 2, 6), (0, 1, 5, 6), (0, 2, 3, 6), (0, 1, 3, 4), (0, 2, 5, 6),
              (0, 3, 4, 6), (1, 2, 4, 6), (0, 2, 4, 6), (0, 1, 4, 5), (0, 2, 4, 5),
              (0, 1, 2, 3), (2, 3, 4, 6), (0, 1, 3, 6)]

# which stage opens which branch depth, and which depth gates the next hub
GATES = [('spine2', 'd0'), ('spine3', 'd2'), ('spine4', 'd4'),
         ('spine5', 'd6'), ('spine6', 'd7')]

AF_X, NV_X = 32, 37          # army/air and navy side by side, far right


def road_cells(branch):
    """One road, rolled from its own seed: uneven rows, drifting spacing."""
    rnd = random.Random('pdv-road-' + branch)
    b = BAND[branch]
    cells = {}
    hub = lambda: b + rnd.choice([2, 3, 3, 3, 4])

    y = rnd.choice([2, 2, 3])
    cells['PDV_%s_review' % branch] = (hub(), y)
    y += rnd.choice([1, 1, 2])
    cells['PDV_%s_spine1' % branch] = (hub(), y)

    for depth in range(8):
        y += rnd.choice([1, 1, 2])
        shape = rnd.choice(ROW_SHAPES)
        stagger = rnd.random() < 0.5
        low = []
        for c, dx in zip(COLS, shape):
            fy = y + (1 if stagger and rnd.random() < 0.45 else 0)
            cells['PDV_%s_%s_%d' % (branch, c, depth)] = (b + dx, fy)
            low.append(fy)
        y = max(low)
        if depth in HUB_ROWS:
            y += 1
            cells['PDV_%s_%s' % (branch, HUB_ROWS[depth])] = (hub(), y)

    y += rnd.choice([1, 1, 2])
    cells['PDV_%s_final' % branch] = (hub(), y)
    return cells


def road_prereqs(branch):
    """id -> list of prerequisite groups; one group = all of them required."""
    pre = {'PDV_%s_review' % branch: [['PDV_four_roads']],
           'PDV_%s_spine1' % branch: [['PDV_%s_review' % branch]]}
    counts = dict(GATES)
    for i in range(2, 7):
        depth = counts['spine%d' % i][1:]
        pre['PDV_%s_spine%d' % (branch, i)] = [
            ['PDV_%s_%s_%s' % (branch, c, depth) for c in COLS]]
    pre['PDV_%s_final' % branch] = [['PDV_%s_spine6' % branch]]

    # every branch depth is opened by a hub, and each depth follows the one above
    opener = {'1': '2', '3': '3', '5': '4', '7': '5'}   # depth -> hub that opens it
    for depth in range(8):
        for c in COLS:
            fid = 'PDV_%s_%s_%d' % (branch, c, depth)
            if depth == 0:
                pre[fid] = [['PDV_%s_spine1' % branch]]
            elif depth in (1, 3, 5, 7):
                pre[fid] = [['PDV_%s_spine%s' % (branch, opener[str(depth)])]]
            else:
                pre[fid] = [['PDV_%s_%s_%d' % (branch, c, depth - 1)]]
    return pre


AF_LAYOUT = {
    'PDV_af_root': (1, 2), 'PDV_af_armour': (0, 3), 'PDV_af_guns': (3, 3),
    'PDV_af_hulls': (0, 4), 'PDV_af_barrels': (3, 4), 'PDV_af_columns': (0, 5),
    'PDV_af_battery': (3, 5), 'PDV_af_combined': (0, 6), 'PDV_af_counterbattery': (3, 6),
    'PDV_af_manual': (1, 7), 'PDV_af_air': (1, 8), 'PDV_af_fighters': (0, 9),
    'PDV_af_airfields': (3, 9), 'PDV_af_radar': (0, 10), 'PDV_af_cas': (3, 10),
    'PDV_af_wing': (0, 11), 'PDV_af_strike': (3, 11), 'PDV_af_divebomber': (1, 12),
    'PDV_af_airdoctrine': (1, 13), 'PDV_af_capstone': (1, 14),
}

NV_LAYOUT = {
    'PDV_nv_root': (1, 2), 'PDV_nv_surface': (0, 3), 'PDV_nv_subs': (3, 3),
    'PDV_nv_cruisers': (0, 4), 'PDV_nv_pens': (3, 4), 'PDV_nv_destroyers': (0, 5),
    'PDV_nv_wolfpack': (3, 5), 'PDV_nv_battleline': (0, 6), 'PDV_nv_mines': (3, 6),
    'PDV_nv_doctrine': (1, 7), 'PDV_nv_coast': (0, 8), 'PDV_nv_marines': (3, 8),
    'PDV_nv_convoys': (0, 9), 'PDV_nv_tradewar': (3, 9), 'PDV_nv_admiralty': (0, 10),
    'PDV_nv_academy': (3, 10), 'PDV_nv_screen': (1, 11), 'PDV_nv_silent': (0, 12),
    'PDV_nv_fleetair': (3, 12), 'PDV_nv_law': (1, 13),
}

AF_PRE = {
    'PDV_af_root': [['PDV_four_roads']],
    'PDV_af_armour': [['PDV_af_root']], 'PDV_af_guns': [['PDV_af_root']],
    'PDV_af_hulls': [['PDV_af_armour']], 'PDV_af_barrels': [['PDV_af_guns']],
    'PDV_af_columns': [['PDV_af_hulls']], 'PDV_af_battery': [['PDV_af_barrels']],
    'PDV_af_combined': [['PDV_af_columns']], 'PDV_af_counterbattery': [['PDV_af_battery']],
    'PDV_af_manual': [['PDV_af_combined', 'PDV_af_counterbattery']],
    'PDV_af_air': [['PDV_af_manual']],
    'PDV_af_fighters': [['PDV_af_air']], 'PDV_af_airfields': [['PDV_af_air']],
    'PDV_af_radar': [['PDV_af_fighters']], 'PDV_af_cas': [['PDV_af_airfields']],
    'PDV_af_wing': [['PDV_af_radar']], 'PDV_af_strike': [['PDV_af_cas']],
    'PDV_af_divebomber': [['PDV_af_wing', 'PDV_af_strike']],
    'PDV_af_airdoctrine': [['PDV_af_divebomber']],
    'PDV_af_capstone': [['PDV_af_airdoctrine']],
}

NV_PRE = {
    'PDV_nv_root': [['PDV_four_roads']],
    'PDV_nv_surface': [['PDV_nv_root']], 'PDV_nv_subs': [['PDV_nv_root']],
    'PDV_nv_cruisers': [['PDV_nv_surface']], 'PDV_nv_pens': [['PDV_nv_subs']],
    'PDV_nv_destroyers': [['PDV_nv_cruisers']], 'PDV_nv_wolfpack': [['PDV_nv_pens']],
    'PDV_nv_battleline': [['PDV_nv_destroyers']], 'PDV_nv_mines': [['PDV_nv_wolfpack']],
    'PDV_nv_doctrine': [['PDV_nv_battleline', 'PDV_nv_mines']],
    'PDV_nv_coast': [['PDV_nv_doctrine']], 'PDV_nv_marines': [['PDV_nv_doctrine']],
    'PDV_nv_convoys': [['PDV_nv_coast']], 'PDV_nv_tradewar': [['PDV_nv_marines']],
    'PDV_nv_admiralty': [['PDV_nv_convoys']], 'PDV_nv_academy': [['PDV_nv_tradewar']],
    'PDV_nv_screen': [['PDV_nv_admiralty', 'PDV_nv_academy']],
    'PDV_nv_silent': [['PDV_nv_screen']], 'PDV_nv_fleetair': [['PDV_nv_screen']],
    'PDV_nv_law': [['PDV_nv_silent', 'PDV_nv_fleetair']],
}


def build():
    cells, pre = {}, {}
    for branch in BAND:
        cells.update(road_cells(branch))
        pre.update(road_prereqs(branch))
    for layout_map, x in ((AF_LAYOUT, AF_X), (NV_LAYOUT, NV_X)):
        for fid, (cx, cy) in layout_map.items():
            cells[fid] = (x + cx, cy)
    pre.update(AF_PRE)
    pre.update(NV_PRE)
    cells.update(TRUNK)
    pre['PDV_four_roads'] = [['PDV_the_directorate']]
    return cells, pre


if __name__ == '__main__':
    cells, pre = build()
    print(len(cells), 'focuses |', len(pre), 'with prerequisites')
    seen = {}
    for k, v in cells.items():
        if v in seen:
            print('COLLISION', k, seen[v], v)
        seen[v] = k
    xs = [x for x, y in cells.values()]
    ys = [y for x, y in cells.values()]
    print('extent x', min(xs), max(xs), '| y', min(ys), max(ys))
