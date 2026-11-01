# -*- coding: utf-8 -*-
"""Every Vyratia focus effect, written to the lore.

Structure per road (cm / dm / fa / mo):
  review    - the road's ideology takes over
  spine1-6  - the army is rebuilt: each spine step trades one debuff for a
              weaker one, and the last step clears the army completely
  c0..c3 x d0..d7 - the body of the road, themed per column
  final     - the culmination of that road

The lore beats that matter (the six fascist support drives before the civil
war, the royalist support drive before the coup, the democratic split into
five nations, the Reich, the two alliance chains) are written out by hand.
"""
import re

# ---------------------------------------------------------------- helpers

CIV = ('random_owned_controlled_state = {\n'
       '\tlimit = { free_building_slots = { building = industrial_complex size > 0 include_locked = yes } }\n'
       '\tadd_building_construction = { type = industrial_complex level = 1 instant_build = yes }\n'
       '}')
MIL = ('random_owned_controlled_state = {\n'
       '\tlimit = { free_building_slots = { building = arms_factory size > 0 include_locked = yes } }\n'
       '\tadd_building_construction = { type = arms_factory level = 1 instant_build = yes }\n'
       '}')
DOCK = ('random_owned_controlled_state = {\n'
        '\tlimit = { is_coastal = yes free_building_slots = { building = dockyard size > 0 include_locked = yes } }\n'
        '\tadd_building_construction = { type = dockyard level = 1 instant_build = yes }\n'
        '}')


def tech(name, category, bonus=0.5, uses=1):
    return ('add_tech_bonus = { name = %s bonus = %.2f uses = %d category = %s }'
            % (name, bonus, uses, category))


# ---------------------------------------------------------------- road theme
# which subject each of the four columns of a road covers
THEME = {
    'cm': {'c0': 'industry', 'c1': 'party', 'c2': 'army', 'c3': 'foreign'},
    'dm': {'c0': 'industry', 'c1': 'liberty', 'c2': 'army', 'c3': 'foreign'},
    'fa': {'c0': 'industry', 'c1': 'party', 'c2': 'army', 'c3': 'foreign'},
    'mo': {'c0': 'estates', 'c1': 'court', 'c2': 'army', 'c3': 'dynasty'},
}

# scale of reward: the democratic road is the lavishly rewarded one, the
# historical communist road the plainest
POWER = {'cm': 1.0, 'dm': 1.35, 'fa': 1.15, 'mo': 1.1}


# ---------------------------------------------------------------- keywords
# name keyword -> what the focus actually does
KEYWORDS = [
    (('motorway', 'road', 'rail', 'canal', 'harbour', 'port'), 'infra'),
    (('bank', 'credit', 'silver', 'currency', 'budget', 'treasury', 'loan'), 'money'),
    (('school', 'academy', 'university', 'learned', 'engineer', 'research'), 'science'),
    (('press', 'radio', 'propaganda', 'ceremon', 'fair', 'festival', 'church'), 'culture'),
    (('tank', 'armour', 'cavalry', 'artillery', 'division', 'regiment', 'corps',
      'guard', 'militia', 'stormtroop', 'officer', 'soldier', 'army', 'arsenal'), 'army'),
    (('navy', 'admiralty', 'fleet', 'dockyard', 'marine', 'convoy', 'submarine', 'cruiser'), 'sea'),
    (('air', 'bomber', 'fighter', 'radar', 'wing'), 'air'),
    (('treaty', 'alliance', 'envoy', 'embassy', 'marriage', 'diplomat', 'pact',
      'protectorate', 'question', 'claim', 'reach', 'corps diplomatique'), 'diplomacy'),
    (('factory', 'industry', 'industrial', 'plantation', 'economy', 'estate', 'guild',
      'farm', 'grain', 'autarky', 'corporate', 'war economy', 'production'), 'industry'),
    (('youth', 'women', 'mother', 'child', 'labour', 'village', 'community', 'man',
      'charity', 'poor', 'nobility', 'crown', 'realm', 'people'), 'society'),
]


def pick(name):
    low = name.lower()
    for words, kind in KEYWORDS:
        if any(w in low for w in words):
            return kind
    return None


# ---------------------------------------------------------------- spine
# each spine step swaps a debuff for a weaker one; the last two clear the army
SPINE_DEBUFF = {
    1: ('PDV_purged_officer_corps', 'PDV_officers_returning'),
    2: ('PDV_hollow_army', 'PDV_army_rebuilding'),
    3: ('PDV_officers_returning', 'PDV_officers_settling'),
    4: ('PDV_army_rebuilding', 'PDV_army_refitting'),
    5: ('PDV_officers_settling', None),
    6: ('PDV_army_refitting', None),
}

# the democratic road works the same chain off in three steps instead of six
DM_SPINE_DEBUFF = {
    1: [('PDV_purged_officer_corps', 'PDV_officers_returning'),
        ('PDV_hollow_army', 'PDV_army_rebuilding')],
    2: [('PDV_officers_returning', 'PDV_officers_settling'),
        ('PDV_army_rebuilding', 'PDV_army_refitting')],
    3: [('PDV_officers_settling', None), ('PDV_army_refitting', None)],
}

SPINE_BUFF = {
    'cm': {1: 'add_army_experience = 25', 2: 'add_army_experience = 30',
           3: 'add_army_experience = 35\nadd_stability = 0.02',
           4: 'add_army_experience = 40\nadd_war_support = 0.03',
           5: 'add_army_experience = 50\nadd_command_power = 25',
           6: 'add_army_experience = 60\nadd_command_power = 35'},
    'dm': {1: 'add_army_experience = 35\nadd_stability = 0.03',
           2: 'add_army_experience = 45\nadd_stability = 0.03',
           3: 'add_army_experience = 55\nadd_command_power = 30',
           4: 'add_army_experience = 60\nadd_command_power = 35',
           5: 'add_army_experience = 70\nadd_command_power = 40',
           6: 'add_army_experience = 80\nadd_command_power = 50'},
    'fa': {1: 'add_army_experience = 30\nadd_war_support = 0.02',
           2: 'add_army_experience = 40\nadd_war_support = 0.03',
           3: 'add_army_experience = 50\nadd_war_support = 0.03',
           4: 'add_army_experience = 55\nadd_war_support = 0.04',
           5: 'add_army_experience = 65\nadd_war_support = 0.04',
           6: 'add_army_experience = 75\nadd_war_support = 0.05'},
    'mo': {1: 'add_army_experience = 20\nadd_command_power = 20',
           2: 'add_army_experience = 25\nadd_command_power = 25',
           3: 'add_army_experience = 30\nadd_command_power = 30',
           4: 'add_army_experience = 35\nadd_command_power = 30',
           5: 'add_army_experience = 40\nadd_command_power = 35',
           6: 'add_army_experience = 50\nadd_command_power = 40'},
}


# ---------------------------------------------------------------- hand written
OVERRIDES = {
    # --- the four openers
    'PDV_cm_review': ('set_politics = { ruling_party = communism elections_allowed = no }\n'
                      'add_popularity = { ideology = communism popularity = 0.15 }\n'
                      'add_stability = 0.04'),
    'PDV_dm_review': ('set_politics = { ruling_party = democratic elections_allowed = yes }\n'
                      'add_popularity = { ideology = democratic popularity = 0.15 }\n'
                      'add_stability = 0.04'),
    # the fascists start on ten per cent and climb five at a time from there
    'PDV_fa_review': ('set_politics = { ruling_party = fascism elections_allowed = no }\n'
                      'add_war_support = 0.04\nadd_stability = -0.02'),
    'PDV_mo_review': ('set_politics = { ruling_party = neutrality elections_allowed = yes }\n'
                      'add_popularity = { ideology = neutrality popularity = 0.15 }\n'
                      'add_stability = 0.03'),

    # --- fascist support drive: six focuses at +5%, which is the thirty per
    #     cent the party needs before it dares the civil war
    'PDV_fa_c0_0': 'add_popularity = { ideology = fascism popularity = 0.05 }\nadd_war_support = 0.02',
    'PDV_fa_c1_0': 'add_popularity = { ideology = fascism popularity = 0.05 }\nadd_war_support = 0.02',
    'PDV_fa_c2_0': 'add_popularity = { ideology = fascism popularity = 0.05 }\nadd_army_experience = 20',
    'PDV_fa_c3_0': 'add_popularity = { ideology = fascism popularity = 0.05 }\nadd_political_power = 25',
    'PDV_fa_c0_1': 'add_popularity = { ideology = fascism popularity = 0.05 }\nadd_stability = 0.02',
    'PDV_fa_c1_1': 'add_popularity = { ideology = fascism popularity = 0.05 }\nadd_stability = 0.02',

    # --- the civil war itself: the industrial south-east rises, the leaders
    #     are killed (event .1), the rump is left leaderless, and thirty days
    #     later the breakaway provinces are recognised (event .2)
    'PDV_fa_c3_3': ('set_politics = { ruling_party = fascism elections_allowed = no last_election = "1939.1.1" election_frequency = 48 }\n'
                    'release = SUN\nrelease = BRR\nrelease = AFR\nrelease = VYR\nrelease = FGT\nrelease = PPS\n'
                    'PPS = { add_ideas = PDV_peoples_defence }\n'
                    'start_civil_war = { ideology = communism size = 0.68 army_ratio = 0.40 navy_ratio = 0.40 air_ratio = 0.30 capital = 361 only_own_territory = yes }\n'
                    'country_event = { id = pdv_vyratia.1 days = 1 }\n'
                    'country_event = { id = pdv_vyratia.2 days = 30 }\n'
                    'add_war_support = 0.10'),

    # --- the Reich
    'PDV_fa_spine6': ('set_cosmetic_tag = PDV_REICH\nadd_ideas = PDV_reich\n'
                      'add_research_slot = 1\nadd_war_support = 0.05'),
    'PDV_fa_final': ('add_ideas = PDV_reich\nadd_stability = 0.05\nadd_war_support = 0.05\n'
                     'add_command_power = 50'),
    'PDV_fa_c3_1': ('if = { limit = { SMH = { exists = yes } } SMH = { country_event = pdv_vyratia.3 } }\n'
                    'add_political_power = 30'),
    'PDV_fa_c3_2': 'add_political_power = 40\nadd_opinion_modifier = { target = COD modifier = pdv_funded_friends }',

    # --- the democratic split: five nations, four of them ours
    'PDV_dm_c3_3': ('add_popularity = { ideology = democratic popularity = 0.05 }\n'
                    'add_stability = 0.03\nadd_political_power = 25'),
    'PDV_dm_spine6': ('release_puppet = SUN\nrelease_puppet = BRR\nrelease_puppet = AFR\nrelease_puppet = VYR\n'
                      'set_cosmetic_tag = PDV_FED\nadd_ideas = PDV_federal_republic\n'
                      'add_research_slot = 1\nadd_stability = 0.08\nadd_political_power = 100'),
    'PDV_dm_final': ('add_ideas = PDV_federal_republic\nadd_stability = 0.08\nadd_research_slot = 1\n'
                     'add_political_power = 75'),

    # --- the royalists
    'PDV_mo_c3_3': ('set_politics = { ruling_party = neutrality elections_allowed = yes }\n'
                    'add_ideas = PDV_crown_restored\nadd_stability = 0.05\nadd_political_power = 50'),
    'PDV_mo_c3_2': ('add_ideas = PDV_rbd_infiltration\nadd_political_power = 25'),
    # the marriage is the first of four steps on the road to Somharhem
    'PDV_mo_c3_0': ('add_political_power = 30\n'
                    'if = { limit = { SMH = { exists = yes } } SMH = { add_opinion_modifier = { target = ROOT modifier = pdv_good_neighbours } } }'),
    # the Cornish Duchy is invited into the Crowned League
    'PDV_mo_c3_1': ('add_political_power = 35\n'
                    'if = { limit = { NOT = { is_in_faction = yes } } create_faction = "The Crowned League" }\n'
                    'if = { limit = { COD = { exists = yes } } COD = { add_to_faction = ROOT } }'),
    # the fourth step: Somharhem is offered the crown's protection
    'PDV_mo_c3_4': ('if = { limit = { SMH = { exists = yes } } SMH = { country_event = pdv_vyratia.3 } }\n'
                    'add_political_power = 40'),
    'PDV_mo_spine6': ('add_ideas = PDV_crown_restored\nadd_stability = 0.05\nadd_political_power = 50\n'
                      'remove_ideas = PDV_officers_settling\nremove_ideas = PDV_army_refitting'),
    'PDV_mo_final': ('add_ideas = PDV_crown_restored\nadd_stability = 0.06\nadd_political_power = 75'),

    # --- the far-right economy pair
    'PDV_econ_patient': ('add_stability = 0.02\nadd_political_power = 25'),
    'PDV_econ_step1': ('remove_ideas = overstretched_industry\n'
                       'add_ideas = overstretched_industry_triage\nadd_stability = 0.02\nadd_political_power = 25'),
    'PDV_econ_step2': ('remove_ideas = overstretched_industry_triage\n'
                       'add_ideas = overstretched_industry_reformed\nadd_stability = 0.02\nadd_political_power = 25'),
    # mid 1939: the last of the economic debts is finally written off
    'PDV_econ_step3': ('remove_ideas = overstretched_industry_reformed\n'
                       'add_stability = 0.03\nadd_political_power = 50'),
    # the gamble: everything at once, and three years to make it pay
    'PDV_econ_force': ('remove_ideas = overstretched_industry\n'
                       'remove_ideas = overstretched_industry_triage\n'
                       'remove_ideas = overstretched_industry_reformed\n'
                       'add_ideas = PDV_forced_economy\n'
                       'country_event = { id = pdv_vyratia.10 days = 1093 }\n'
                       'add_stability = 0.02'),
    'PDV_print_money': 'add_ideas = PDV_print_money\nadd_political_power = 25',
    'PDV_generals_power': ('add_ideas = PDV_final_show_of_power\n'
                           'add_command_power = 25\nadd_army_experience = 25'),
    'PDV_propaganda_supremacy': ('add_ideas = PDV_propaganda_supremacy\n'
                                 'add_stability = 0.03\nadd_war_support = 0.03'),

    'PDV_cm_final': ('add_ideas = PDV_rebuilt_staff\nadd_stability = 0.05\nadd_political_power = 75\n'
                     'add_research_slot = 1'),
}


# --------------------------------------------------------------- body effects
def _body(kind, depth, road):
    """The effect of an ordinary row focus, scaled by how deep down the road it sits."""
    p = POWER[road]
    step = depth

    if kind == 'infra':
        out = ['add_stability = 0.02', tech('cdw_pdv_%s_infra' % road, 'industry', 0.5, 1)]
        if step >= 3:
            out.append("random_owned_controlled_state = {\n\tlimit = { free_building_slots = { building = infrastructure size > 0 include_locked = yes } }\n\tadd_building_construction = { type = infrastructure level = 1 instant_build = yes }\n}")
        return '\n'.join(out)

    if kind == 'money':
        out = ['add_stability = %.2f' % (0.02 * p), 'add_political_power = %d' % int(20 * p)]
        if step >= 4:
            out.append('consumer_goods_factor = -0.02')
        return '\n'.join(out)

    if kind == 'science':
        return tech('cdw_pdv_%s_science' % road, 'electronics', 0.5, 1) + '\nadd_research_slot = 0'

    if kind == 'culture':
        return ('add_stability = %.2f' % (0.02 * p)) + '\nadd_political_power = %d' % int(15 * p)

    if kind == 'army':
        out = ['add_army_experience = %d' % int(20 + 5 * step * p)]
        if step >= 3:
            out.append('add_command_power = %d' % int(15 * p))
        return '\n'.join(out)

    if kind == 'sea':
        out = ['add_navy_experience = %d' % int(20 + 5 * step * p)]
        if step >= 4:
            out.append(tech('cdw_pdv_%s_naval' % road, 'cruiser', 0.4, 1))
        return '\n'.join(out)

    if kind == 'air':
        out = ['add_air_experience = %d' % int(20 + 5 * step * p)]
        if step >= 4:
            out.append(tech('cdw_pdv_%s_air' % road, 'light_fighter', 0.4, 1))
        return '\n'.join(out)

    if kind == 'diplomacy':
        return 'add_political_power = %d\nadd_stability = 0.02' % int(25 * p)

    if kind == 'industry':
        out = []
        if step in (1, 4, 7):
            out.append(CIV)
        else:
            out.append(tech('cdw_pdv_%s_industry' % road, 'industry', 0.5, 1))
        out.append('add_stability = 0.02')
        return '\n'.join(out)

    if kind == 'society':
        out = ['add_stability = %.2f' % (0.02 * p)]
        if step >= 5:
            out.append('add_manpower = %d' % int(20000 * p))
        return '\n'.join(out)

    # fallback: something small but not political power alone
    return 'add_stability = 0.02\nadd_army_experience = 10'


DEMOCRATIC_PRINCIPLES = [('free speech', 'freedom of speech'), ('free press', 'a free press'),
                         ('assembly', 'the right to assemble'), ('courts', 'independent courts'),
                         ('unions', 'free trade unions'), ('ballot', 'a secret ballot'),
                         ('constitution', 'a written constitution'), ('elections', 'free elections')]

# the four breakaway nations the fascists have to fight their way back into
WARGOAL = {
    'PDV_fa_c0_5': 'FGT', 'PDV_fa_c1_5': 'PPS', 'PDV_fa_c2_6': 'SUN', 'PDV_fa_c3_6': 'AFR',
}


def effect_for(fid, name):
    """Effect body for any Vyratia focus."""
    if fid in OVERRIDES:
        return OVERRIDES[fid]

    # --- the democratic road spends its second column building a democracy
    m0 = re.match(r'PDV_dm_c1_(\d)', fid)
    if m0:
        return ('add_popularity = { ideology = democratic popularity = 0.05 }\n'
                'add_stability = 0.02\nadd_political_power = 15')

    # --- the royalists spend their first six focuses on the old families
    m1 = re.match(r'PDV_mo_(c[0-3])_0$|PDV_mo_(c[0-1])_1$', fid)
    if m1:
        return ('add_popularity = { ideology = neutrality popularity = 0.07 }\n'
                'add_political_power = 15\nadd_stability = 0.01')

    # --- once the war is won the Reich goes back for the provinces
    if fid in WARGOAL:
        tag = WARGOAL[fid]
        return ('add_war_support = 0.03\n'
                'if = { limit = { %s = { exists = yes } } create_wargoal = { type = annex_everything target = %s } }'
                % (tag, tag))

    parts = fid.split('_')
    if len(parts) < 3:
        return 'add_political_power = 25'

    if parts[1] == 'af':                                    # army / air side tree
        return _side(fid, parts[2], 'af')
    if parts[1] == 'nv':                                    # navy side tree
        return _side(fid, parts[2], 'nv')

    road, kind = parts[1], parts[2]

    if kind == 'review':
        return 'add_political_power = 25'
    if kind == 'spine1' and road not in ('cm', 'dm', 'fa', 'mo'):
        return 'add_political_power = 25'

    if kind.startswith('spine'):
        step = int(kind[5:])
        lines = []
        if road == 'dm':
            for old, new in DM_SPINE_DEBUFF.get(step, []):
                lines.append('remove_ideas = %s' % old)
                if new:
                    lines.append('add_ideas = %s' % new)
        else:
            old, new = SPINE_DEBUFF[step]
            lines.append('remove_ideas = %s' % old)
            if new:
                lines.append('add_ideas = %s' % new)
        lines.append(SPINE_BUFF[road][step])
        return '\n'.join(lines)

    # ordinary row focus: PDV_<road>_<c?>_<depth>
    m = re.match(r'PDV_(\w\w)_(c\d)_(\d)', fid)
    if not m:
        return 'add_political_power = 25'
    col, depth = m.group(2), int(m.group(3))
    theme = THEME[road][col]
    flavour = pick(name)
    return _body(flavour or theme, depth, road)


def _side(fid, kind, tree):
    """Army/air and navy side trees: research and a short leash on factories."""
    # three military factories across the whole army/air branch
    if tree == 'af' and kind in ('manual', 'air', 'capstone'):
        return ('add_army_experience = 40\n' + tech('cdw_pdv_af_industry', 'infantry_tech', 0.5, 1)
                + '\n' + MIL)
    # three dockyards across the whole navy branch
    if tree == 'nv' and kind in ('pens', 'destroyers', 'law'):
        return ('add_navy_experience = 40\n' + tech('cdw_pdv_nv_industry', 'cruiser', 0.5, 1)
                + '\n' + DOCK)
    if kind in ('root', 'capstone', 'law'):
        return 'add_political_power = 25\nadd_command_power = 20'
    if kind in ('armour', 'guns', 'hulls', 'barrels'):
        return ('add_army_experience = 30\n' + tech('cdw_pdv_%s_land' % tree, 'infantry_tech', 0.5, 1))
    if kind in ('columns', 'battery', 'combined', 'counterbattery', 'manual'):
        return 'add_army_experience = 40\n' + tech('cdw_pdv_%s_manual' % tree, 'artillery', 0.5, 1)
    if kind in ('air', 'fighters', 'airfields', 'radar', 'cas', 'wing', 'strike',
                'divebomber', 'airdoctrine'):
        return 'add_air_experience = 35\n' + tech('cdw_pdv_%s_air' % tree, 'light_fighter', 0.5, 1)
    if kind in ('surface', 'subs', 'cruisers', 'pens', 'destroyers', 'wolfpack',
                'battleline', 'mines', 'doctrine', 'coast', 'marines', 'convoys',
                'tradewar', 'admiralty', 'academy', 'screen', 'silent', 'fleetair'):
        return 'add_navy_experience = 40\n' + tech('cdw_pdv_%s_naval' % tree, 'cruiser', 0.5, 1)
    return 'add_political_power = 25'
