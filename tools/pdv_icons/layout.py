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
LOC = MOD + 'localisation/english/replace/pdv_vyratia_l_english.yml'

BAND = {'cm': 0, 'dm': 9, 'fa': 18, 'mo': 27}   # eight columns each, one column of air
COLS = ('c0', 'c1', 'c2', 'c3')                   # the four focuses in a row

TRUNK = {'PDV_the_directorate': (20, 0), 'PDV_four_roads': (20, 1)}
ROAD_TOP = 3            # every road opens on this row, so the four choices line up

# rows of four, and the hubs that demand all four. Nothing here is a fixed
# rhythm: each road rolls its own row shapes and spacing, so the four roads
# read as hand-built branches rather than four copies of one lattice.
HUB_ROWS = {0: 'spine2', 2: 'spine3', 4: 'spine4', 6: 'spine5', 7: 'spine6'}

# where a row's four focuses stand inside its eight-column band: never closer
# than two columns. Which of the four branch focuses takes which spot is
# shuffled every row, so no column ever lines up down a road.
ROW_SHAPES = [(0, 2, 4, 6), (0, 2, 4, 7), (0, 2, 5, 7), (0, 3, 5, 7), (1, 3, 5, 7),
              (0, 2, 4, 6), (1, 3, 6, 8), (0, 2, 4, 8), (0, 3, 6, 8)]

# which stage opens which branch depth, and which depth gates the next hub
GATES = [('spine2', 'd0'), ('spine3', 'd2'), ('spine4', 'd4'),
         ('spine5', 'd6'), ('spine6', 'd7')]

AF_X, NV_X = 37, 42          # army/air and navy side by side, far right


def road_cells(branch):
    """One road, rolled from its own seed. Rows are shuffled, unevenly spaced and
    never mirror another road: the opener shares a line with the other three
    roads, everything under it is that road's own shape."""
    rnd = random.Random('pdv-road-rolled-' + branch)
    b = BAND[branch]
    spread = rnd.choice([6, 6, 7, 7])            # each road uses its own width
    palette = [s for s in ROW_SHAPES if max(s) <= spread] or [(0, 2, 4, 6)]
    cells = {'PDV_%s_review' % branch: (b + rnd.choice([3, 4, 5]), ROAD_TOP)}

    y = ROAD_TOP + rnd.choice([2, 3, 3])
    cells['PDV_%s_spine1' % branch] = (b + rnd.choice([2, 3, 4, 5, 6]), y)

    for depth in range(8):
        y += rnd.choice([1, 1, 2])
        shape = list(rnd.choice(palette))
        if max(shape) < spread and rnd.random() < 0.3:
            shape = [d + 1 for d in shape]
        order = list(COLS)
        rnd.shuffle(order)
        for c, dx in zip(order, shape):
            cells['PDV_%s_%s_%d' % (branch, c, depth)] = (b + dx, y)
        if depth in HUB_ROWS:
            free = [x for x in range(spread + 1)
                    if all(abs(x - dx) >= 2 for dx in shape)]
            free = free or [x for x in range(spread + 1) if x not in shape] or [3]
            y += rnd.choice([1, 1, 2])
            cells['PDV_%s_%s' % (branch, HUB_ROWS[depth])] = (b + rnd.choice(free), y)

    cells['PDV_%s_final' % branch] = (b + rnd.choice([3, 4, 5]), y + 1)
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


# ---------------------------------------------------------------------------
# The far-right economy pair, kept clear of everything else: the patient road
# on the left, the forced road on the right, three follow-ups under the forced
# one. The player will place these by hand, so they stand alone.
ECON = {
    'PDV_econ_patient': {
        'pos': (49, 3), 'pre': [], 'mutex': ['PDV_econ_force'],
        'avail': ['date > 1936.3.1'],
    },
    'PDV_econ_step1': {
        'pos': (49, 5), 'pre': [['PDV_econ_patient']], 'mutex': [],
        'avail': ['date > 1936.12.1'],
    },
    'PDV_econ_step2': {
        'pos': (49, 7), 'pre': [['PDV_econ_step1']], 'mutex': [],
        'avail': ['date > 1937.9.1'],
    },
    'PDV_econ_step3': {
        'pos': (49, 9), 'pre': [['PDV_econ_step2']], 'mutex': [],
        'avail': ['date > 1939.6.1'],
    },
    'PDV_econ_force': {
        'pos': (54, 3), 'pre': [], 'mutex': ['PDV_econ_patient'],
        'avail': ['date > 1937.1.1', 'date < 1937.2.1'],
    },
    'PDV_print_money': {
        'pos': (52, 6), 'pre': [['PDV_econ_force']], 'mutex': [], 'avail': [],
    },
    'PDV_generals_power': {
        'pos': (54, 6), 'pre': [['PDV_econ_force']], 'mutex': [], 'avail': [],
    },
    'PDV_propaganda_supremacy': {
        'pos': (56, 6), 'pre': [['PDV_econ_force']], 'mutex': [], 'avail': [],
    },
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
    for fid, spec_ in ECON.items():
        cells[fid] = spec_['pos']
        if spec_['pre']:
            pre[fid] = spec_['pre']
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
