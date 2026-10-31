# -*- coding: utf-8 -*-
"""Applies the new layout, prerequisites and lore tooltips to PDV_vyratia.txt."""
import re
import sys

sys.path.insert(0, '/home/user/Marnix/tools/pdv_icons')
import layout
import lore

TREE = layout.TREE
LOC = layout.LOC


def focus_blocks(src):
    """[(start, end, text)] of every brace-matched focus block."""
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
        out.append((j, m + 1, src[j:m + 1]))
        i = m + 1


def field(block, name):
    m = re.search(r'\n\t\t%s = (\S+)' % name, block)
    return m.group(1) if m else None


def inner(block, name):
    m = re.search(r'\n\t\t%s = \{([\s\S]*?)\n\t\t\}' % name, block)
    return m.group(1) if m else None


def inline(block, name):
    m = re.search(r'\n\t\t%s = \{([^}]*)\}' % name, block)
    return m.group(1) if m else None


def main():
    cells, pre = layout.build()
    src = open(TREE, encoding='utf-8-sig').read()
    blocks = focus_blocks(src)
    assert len(blocks) == 202, len(blocks)
    header = src[:blocks[0][0]]
    tail = src[blocks[-1][1]:]
    assert 'continuous_focus_position' in tail

    body = []
    for start, end, block in blocks:
        fid = field(block, 'id')
        assert fid in cells, fid
        x, y = cells[fid]
        icon = field(block, 'icon')
        cost = field(block, 'cost')
        mutex = inline(block, 'mutually_exclusive')
        reward = inner(block, 'completion_reward')
        assert icon and cost and reward is not None, fid

        lines = ['', '\tfocus = {',
                 '\t\tid = %s' % fid,
                 '\t\ticon = %s' % icon,
                 '\t\tx = %d' % x,
                 '\t\ty = %d' % y,
                 '\t\tcost = %s' % cost]
        if mutex is not None:
            assert 'prerequisite' not in mutex
            lines.append('\t\tmutually_exclusive = {%s}' % mutex)
        if fid in pre:
            lines.append('\t\tprerequisite = { %s }'
                         % ' '.join('focus = %s' % t for g in pre[fid] for t in g))
        lines += ['\t\tcompletion_reward = {',
                  '\t\t\tcustom_effect_tooltip = %s_desc' % fid,
                  reward.strip('\n'),
                  '\t\t}',
                  '\t}']
        body.append('\n'.join(lines))

    footer = ('\n\tcontinuous_focus_position = {\n\t\tx = 14\n\t\ty = 1200\n\t}\n}\n')
    new = header.rstrip('\n') + '\n' + ''.join(body) + footer
    open(TREE, 'w', encoding='utf-8', newline='\n').write(new)

    # ---- localisation
    loc = open(LOC, encoding='utf-8-sig').read()
    missing = []
    for fid, text in lore.LORE.items():
        pat = re.compile(r'^( %s_desc:0 )"[^"]*"' % re.escape(fid), re.M)
        if not pat.search(loc):
            missing.append(fid)
            continue
        loc = pat.sub(lambda m: '%s"%s"' % (m.group(1), text.replace('"', "'")), loc)
    open(LOC, 'w', encoding='utf-8-sig', newline='\n').write(loc)
    print('focuses rewritten:', len(body), '| lore entries:', len(lore.LORE),
          '| loc keys missing:', len(missing))
    if missing:
        print(missing)


if __name__ == '__main__':
    main()
