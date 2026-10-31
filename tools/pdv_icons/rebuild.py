# -*- coding: utf-8 -*-
"""Rebuilds PDV_vyratia.txt: new lattice layout, no-skip gating, vanilla icons,
varied effects, lore tooltips. Also rewrites PDV_ideas.txt with the road spirits.
"""
import re
import sys

sys.path.insert(0, '/home/user/Marnix/tools/pdv_icons')
import layout
import spec

TREE, LOC = layout.TREE, layout.LOC
IDEAS = layout.MOD + 'common/ideas/PDV_ideas.txt'


def focus_blocks(src):
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


def field(block, name):
    m = re.search(r'\n\t\t%s = (\S+)' % name, block)
    return m.group(1) if m else None


def inline(block, name):
    m = re.search(r'\n\t\t%s = \{([^}]*)\}' % name, block)
    return m.group(1) if m else None


HUB_IDEA_RE = re.compile(r'^\s*add_ideas = PDV_(state_plan|party_state|republic_charter|open_society|'
                         r'corporate_economy|reich_doctrine|army_of_the_crown)\s*$')


def reward_of(block):
    m = re.search(r'\n\t\tcompletion_reward = \{([\s\S]*?)\n\t\t\}', block)
    body = m.group(1)
    keep = [l for l in body.split('\n')
            if 'custom_effect_tooltip' not in l and not HUB_IDEA_RE.match(l)]
    return '\n'.join(keep).strip('\n')


def pick_icon(fid, name, sprites):
    if fid in spec.ICON_BY_ID:
        return spec.ICON_BY_ID[fid]
    low = name.lower()
    for kw, icon in spec.ICON_RULES:
        if kw in low:
            return icon
    return spec.BRANCH_ICON.get(fid.split('_')[1], 'GFX_goal_generic_political_pressure')


def main():
    cells, pre = layout.build()
    src = open(TREE, encoding='utf-8-sig').read()
    loc = open(LOC, encoding='utf-8-sig').read()
    names = dict(re.findall(r'^ (PDV_\w+?):0 "([^"]*)"', loc, re.M))
    gfx = open(layout.MOD + 'Interface/goals.gfx', encoding='utf-8-sig').read()
    sprites = set(re.findall(r'name = "(GFX_goal_[^"]+)"', gfx))

    blocks = focus_blocks(src)
    assert len(blocks) == 202, len(blocks)

    body = []
    for block in blocks:
        fid = field(block, 'id')
        assert fid in cells, fid
        x, y = cells[fid]
        icon = pick_icon(fid, names.get(fid, fid), sprites)
        assert icon in sprites or icon == 'GFX_goal_support_neutrality', (fid, icon)
        cost = field(block, 'cost')
        # only the four ideological reviews stay exclusive: everything else is
        # required by the hub above it, so an exclusive pair would dead-end it
        mutex = inline(block, 'mutually_exclusive') if fid.endswith('_review') else None
        fx = spec.FX.get(fid, reward_of(block))

        parts = fid.split('_')
        if len(parts) > 2 and parts[1] in spec.HUB_IDEAS:
            extra = spec.HUB_IDEAS[parts[1]].get(parts[2])
            if extra:
                fx = 'add_ideas = %s\n\t\t\t%s' % (extra, fx.lstrip('\t '))

        lines = ['', '\tfocus = {',
                 '\t\tid = %s' % fid,
                 '\t\ticon = %s' % icon,
                 '\t\tx = %d' % x,
                 '\t\ty = %d' % y,
                 '\t\tcost = %s' % cost]
        if mutex is not None:
            others = re.findall(r'focus = (\S+)', mutex)
            lines.append('\t\tmutually_exclusive = { %s }'
                         % ' '.join('focus = %s' % o for o in others))
        if fid in pre:
            lines.append('\t\tprerequisite = { %s }'
                         % ' '.join('focus = %s' % t for g in pre[fid] for t in g))
        lines += ['\t\tcompletion_reward = {',
                  '\t\t\tcustom_effect_tooltip = %s_desc' % fid,
                  '\t\t\t' + fx.strip('\n'),
                  '\t\t}',
                  '\t}']
        body.append('\n'.join(lines))

    header = '''# Vyratia (PDV) - four roads out of the Directorate, forty focuses each, plus army/air and navy.
# All four roads open side by side at the top. Each road is a lattice: a row of four focuses,
# then a hub that requires all four of them, then the next row. The middle cannot be rushed,
# because the middle is gated by the sides. Army/air and navy stand side by side at the far right.
focus_tree = {
\tid = pdv_focus
\tcountry = {
\t\tfactor = 0
\t\tmodifier = {
\t\t\tadd = 50
\t\t\ttag = PDV
\t\t}
\t}
'''
    footer = '\n\tcontinuous_focus_position = {\n\t\tx = 15\n\t\ty = 1200\n\t}\n}\n'
    open(TREE, 'w', encoding='utf-8', newline='\n').write(header + ''.join(body) + footer)

    # ---- ideas file: emit every spirit inside the country block
    out = ['# Vyratia (PDV) - spirits used by the four roads.\nideas = {\n\n\tcountry = {\n']
    for idea, (picture, mods) in spec.IDEAS.items():
        out.append('\n\t\t%s = {\n\t\t\tpicture = %s\n\t\t\tmodifier = {\n' % (idea, picture))
        for k, v in mods:
            out.append('\t\t\t\t%s = %.2f\n' % (k, v))
        out.append('\t\t\t}\n\t\t}\n')
    out.append('\t}\n\n}\n')
    open(IDEAS, 'w', encoding='utf-8', newline='\n').write(''.join(out))

    # ---- localisation for the new spirits
    add = ''.join(' %s:0 "%s"\n %s_desc:0 "%s"\n' % (k, v[0], k, v[1])
                  for k, v in spec.NEW_IDEA_LOC.items())
    if 'PDV_state_plan:' not in loc:
        loc = loc.replace(' PDV_rebuilt_staff:0', add + '\n PDV_rebuilt_staff:0', 1)
        open(LOC, 'w', encoding='utf-8-sig', newline='\n').write(loc)

    icons = {}
    for b in body:
        icons[field(b, 'id')] = field(b, 'icon')
    print('focuses:', len(body), '| distinct icons:', len(set(icons.values())))
    print('pp-only left:', sum(1 for b in body
                               if re.search(r'completion_reward = \{([\s\S]*?)\n\t\t\}', b).group(1).strip()
                               .count('=') <= 1))


if __name__ == '__main__':
    main()
