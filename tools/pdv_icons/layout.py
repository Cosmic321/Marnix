# -*- coding: utf-8 -*-
"""Re-lays out the Vyratia focus tree and wires the lore tooltips.

Four roads stand side by side across the top (the four mutually exclusive
openings at the same height), each one descends as a braided ladder: the spine
zig-zags down the middle while four branches grow out to either side, open in
two waves and are pinned back to the spine at the halfway checkpoint. Army/air
and navy sit in the rightmost columns.
"""
import re

MOD = '/home/user/Marnix/CosmicDaWinner/'
TREE = MOD + 'common/national_focus/PDV_vyratia.txt'
LOC = MOD + 'Localisation/English/replace/pdv_vyratia_l_english.yml'

BAND = {'cm': 0, 'dm': 8, 'fa': 16, 'mo': 24}      # left column of each road (7 wide)
AF_NV_X = 32                                        # far-right column group

TRUNK = {'PDV_the_directorate': (15, 0), 'PDV_four_roads': (15, 1)}

SPINE_Y = [3, 8, 13, 18, 22, 24]     # spine 1..6
FINAL_Y = 26

# each branch of eight focuses is a ribbon that snakes through a 3x3 block;
# the blocks alternate left and right down the road, one after another
SNAKE_R = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2)]
SNAKE_L = [(2, 0), (1, 0), (0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (1, 2)]
BLOCKS = {'c0': (0, 5, 'L', 2), 'c1': (4, 9, 'R', 3), 'c2': (0, 14, 'L', 4), 'c3': (4, 19, 'R', 5)}


def road_cells(branch):
    """id -> (x, y): trunk down the middle, ribbon blocks braided left and right."""
    b = BAND[branch]
    cells = {'PDV_%s_review' % branch: (b + 3, 2)}
    for i, y in enumerate(SPINE_Y):
        cells['PDV_%s_spine%d' % (branch, i + 1)] = (b + 3, y)
    cells['PDV_%s_final' % branch] = (b + 3, FINAL_Y)
    for c, (dx, y0, side, _) in BLOCKS.items():
        pattern = SNAKE_L if side == 'L' else SNAKE_R
        for i, (cx, cy) in enumerate(pattern):
            cells['PDV_%s_%s_%d' % (branch, c, i)] = (b + dx + cx, y0 + cy)
    return cells


def road_prereqs(branch):
    """id -> list of prerequisite groups (each group is an AND list, groups are OR)."""
    pre = {}
    pre['PDV_%s_review' % branch] = [['PDV_four_roads']]
    pre['PDV_%s_spine1' % branch] = [['PDV_%s_review' % branch]]
    for i in range(2, 7):
        pre['PDV_%s_spine%d' % (branch, i)] = [['PDV_%s_spine%d' % (branch, i - 1)]]
    pre['PDV_%s_final' % branch] = [['PDV_%s_spine6' % branch]]
    for c, (dx, y0, side, gate) in BLOCKS.items():
        first = 'PDV_%s_%s_0' % (branch, c)
        # each branch opens only once the road has advanced to it
        pre[first] = [['PDV_%s_spine%d' % (branch, gate - 1)]]
        for i in range(1, 8):
            pre['PDV_%s_%s_%d' % (branch, c, i)] = [['PDV_%s_%s_%d' % (branch, c, i - 1)]]
        # and it cannot be finished before the road moves on again
        pre['PDV_%s_%s_6' % (branch, c)] = [['PDV_%s_%s_5' % (branch, c),
                                             'PDV_%s_spine%d' % (branch, gate)]]
    return pre


def side_tree_cells():
    """army/air and navy keep their shapes, shifted to the far right."""
    cells = {}
    af = {
        'PDV_af_root': (2, 2), 'PDV_af_armour': (0, 3), 'PDV_af_guns': (4, 3),
        'PDV_af_hulls': (0, 4), 'PDV_af_barrels': (4, 4), 'PDV_af_columns': (0, 5),
        'PDV_af_battery': (4, 5), 'PDV_af_combined': (0, 6), 'PDV_af_counterbattery': (4, 6),
        'PDV_af_manual': (2, 7), 'PDV_af_air': (2, 8), 'PDV_af_fighters': (0, 9),
        'PDV_af_cas': (4, 9), 'PDV_af_radar': (0, 10), 'PDV_af_airfields': (2, 10),
        'PDV_af_strike': (4, 10), 'PDV_af_wing': (0, 11), 'PDV_af_divebomber': (4, 11),
        'PDV_af_airdoctrine': (2, 12), 'PDV_af_capstone': (2, 13),
    }
    nv = {
        'PDV_nv_root': (2, 15), 'PDV_nv_surface': (0, 16), 'PDV_nv_subs': (4, 16),
        'PDV_nv_cruisers': (0, 17), 'PDV_nv_pens': (4, 17), 'PDV_nv_destroyers': (0, 18),
        'PDV_nv_wolfpack': (4, 18), 'PDV_nv_battleline': (0, 19), 'PDV_nv_mines': (4, 19),
        'PDV_nv_screen': (0, 20), 'PDV_nv_silent': (4, 20), 'PDV_nv_doctrine': (2, 21),
        'PDV_nv_coast': (0, 22), 'PDV_nv_marines': (4, 22), 'PDV_nv_convoys': (0, 23),
        'PDV_nv_tradewar': (4, 23), 'PDV_nv_admiralty': (0, 24), 'PDV_nv_academy': (4, 24),
        'PDV_nv_fleetair': (2, 25), 'PDV_nv_law': (2, 26),
    }
    for d in (af, nv):
        for k, (x, y) in d.items():
            cells[k] = (AF_NV_X + x, y)
    return cells


def side_tree_prereqs():
    pre = {
        'PDV_af_root': [['PDV_four_roads']],
        'PDV_af_armour': [['PDV_af_root']], 'PDV_af_guns': [['PDV_af_root']],
        'PDV_af_hulls': [['PDV_af_armour']], 'PDV_af_barrels': [['PDV_af_guns']],
        'PDV_af_columns': [['PDV_af_hulls']], 'PDV_af_battery': [['PDV_af_barrels']],
        'PDV_af_combined': [['PDV_af_columns']], 'PDV_af_counterbattery': [['PDV_af_battery']],
        'PDV_af_manual': [['PDV_af_combined', 'PDV_af_counterbattery']],
        'PDV_af_air': [['PDV_af_manual']],
        'PDV_af_fighters': [['PDV_af_air']], 'PDV_af_cas': [['PDV_af_air']],
        'PDV_af_radar': [['PDV_af_fighters']], 'PDV_af_airfields': [['PDV_af_air']],
        'PDV_af_strike': [['PDV_af_cas']], 'PDV_af_wing': [['PDV_af_radar']],
        'PDV_af_divebomber': [['PDV_af_strike']],
        'PDV_af_airdoctrine': [['PDV_af_wing', 'PDV_af_divebomber', 'PDV_af_airfields']],
        'PDV_af_capstone': [['PDV_af_airdoctrine']],
        'PDV_nv_root': [['PDV_four_roads']],
        'PDV_nv_surface': [['PDV_nv_root']], 'PDV_nv_subs': [['PDV_nv_root']],
        'PDV_nv_cruisers': [['PDV_nv_surface']], 'PDV_nv_pens': [['PDV_nv_subs']],
        'PDV_nv_destroyers': [['PDV_nv_cruisers']], 'PDV_nv_wolfpack': [['PDV_nv_pens']],
        'PDV_nv_battleline': [['PDV_nv_destroyers']], 'PDV_nv_mines': [['PDV_nv_wolfpack']],
        'PDV_nv_screen': [['PDV_nv_battleline']], 'PDV_nv_silent': [['PDV_nv_mines']],
        'PDV_nv_doctrine': [['PDV_nv_screen', 'PDV_nv_silent']],
        'PDV_nv_coast': [['PDV_nv_doctrine']], 'PDV_nv_marines': [['PDV_nv_doctrine']],
        'PDV_nv_convoys': [['PDV_nv_coast']], 'PDV_nv_tradewar': [['PDV_nv_marines']],
        'PDV_nv_admiralty': [['PDV_nv_convoys']], 'PDV_nv_academy': [['PDV_nv_tradewar']],
        'PDV_nv_fleetair': [['PDV_nv_admiralty', 'PDV_nv_academy']],
        'PDV_nv_law': [['PDV_nv_fleetair']],
    }
    return pre


def build():
    cells, pre = {}, {}
    for branch in BAND:
        cells.update(road_cells(branch))
        pre.update(road_prereqs(branch))
    cells.update(side_tree_cells())
    pre.update(side_tree_prereqs())
    cells.update(TRUNK)
    pre['PDV_four_roads'] = [['PDV_the_directorate']]
    return cells, pre


if __name__ == '__main__':
    cells, pre = build()
    print(len(cells), 'focuses', len(pre), 'with prerequisites')
    seen = {}
    for k, v in cells.items():
        if v in seen:
            print('COLLISION', k, seen[v], v)
        seen[v] = k
    print('extent x', min(x for x, y in cells.values()), max(x for x, y in cells.values()),
          'y', min(y for x, y in cells.values()), max(y for x, y in cells.values()))
