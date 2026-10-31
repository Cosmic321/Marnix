# -*- coding: utf-8 -*-
"""Effects, national spirits and vanilla icons for the Vyratia tree."""

# ---------------------------------------------------------------------------
# effects that replace the old "add_political_power = N" placeholders
# ---------------------------------------------------------------------------
BUILD_CIV = '''random_owned_controlled_state = {
				limit = { free_building_slots = { building = industrial_complex size > 0 include_locked = yes } }
				add_building_construction = { type = industrial_complex level = %d instant_build = yes }
			}'''
BUILD_MIL = '''random_owned_controlled_state = {
				limit = { free_building_slots = { building = arms_factory size > 0 include_locked = yes } }
				add_building_construction = { type = arms_factory level = %d instant_build = yes }
			}'''
BUILD_INFRA = '''random_owned_controlled_state = {
				limit = { free_building_slots = { building = infrastructure size > 0 include_locked = yes } }
				add_building_construction = { type = infrastructure level = %d instant_build = yes }
			}'''

FX = {
    'PDV_four_roads': 'add_political_power = 25\n\t\t\tadd_command_power = 25',

    # ------------------------------------------------------------- communist
    'PDV_cm_c0_0': BUILD_CIV % 2,
    'PDV_cm_c0_2': BUILD_MIL % 1 + '\n\t\t\tadd_war_support = 0.02',
    'PDV_cm_c0_4': 'add_tech_bonus = { name = cdw_pdv_bank_research bonus = 0.5 uses = 1 category = industry }\n\t\t\tadd_stability = 0.02',
    'PDV_cm_c0_6': BUILD_MIL % 2,
    'PDV_cm_c0_7': 'add_research_slot = 1\n\t\t\tadd_stability = 0.03',
    'PDV_cm_c1_1': 'add_manpower = 25000\n\t\t\tadd_stability = 0.02',
    'PDV_cm_c1_3': 'add_manpower = 30000\n\t\t\tadd_political_power = 25',
    'PDV_cm_c1_5': 'add_stability = 0.03\n\t\t\tadd_war_support = 0.02',
    'PDV_cm_c3_0': 'add_command_power = 30\n\t\t\tadd_political_power = 25',
    'PDV_cm_c3_2': 'add_war_support = 0.04\n\t\t\tadd_army_experience = 25',
    'PDV_cm_c3_4': 'add_stability = 0.03\n\t\t\tadd_command_power = 25',
    'PDV_cm_c3_6': 'add_war_support = 0.03\n\t\t\tadd_equipment_to_stockpile = { type = infantry_equipment amount = 1500 }',
    'PDV_cm_c3_7': 'add_war_support = 0.05\n\t\t\tadd_army_experience = 50',

    # ------------------------------------------------------------ democratic
    'PDV_dm_c0_0': 'add_stability = 0.03\n\t\t\tadd_command_power = 25',
    'PDV_dm_c0_2': 'add_tech_bonus = { name = cdw_pdv_bank_research bonus = 0.5 uses = 1 category = industry }\n\t\t\tadd_stability = 0.02',
    'PDV_dm_c0_4': BUILD_CIV % 1 + '\n\t\t\tadd_stability = 0.02',
    'PDV_dm_c0_6': BUILD_INFRA % 2,
    'PDV_dm_c0_7': 'add_equipment_to_stockpile = { type = convoy amount = 250 }\n\t\t\tadd_political_power = 40',
    'PDV_dm_c1_1': 'add_manpower = 25000\n\t\t\tadd_stability = 0.03',
    'PDV_dm_c1_3': 'add_stability = 0.04\n\t\t\tadd_political_power = 40',
    'PDV_dm_c1_5': 'add_stability = 0.04\n\t\t\tadd_command_power = 25',
    'PDV_dm_c3_0': 'add_command_power = 30\n\t\t\tadd_political_power = 25',
    'PDV_dm_c3_2': 'add_war_support = 0.03\n\t\t\tadd_navy_experience = 25',
    'PDV_dm_c3_4': 'add_stability = 0.03\n\t\t\tadd_command_power = 25',
    'PDV_dm_c3_6': 'add_stability = 0.04\n\t\t\tadd_equipment_to_stockpile = { type = support_equipment amount = 1000 }',
    'PDV_dm_c3_7': 'add_tech_bonus = { name = cdw_pdv_century_research bonus = 0.5 uses = 2 category = industry }\n\t\t\tadd_political_power = 50',

    # --------------------------------------------------------------- fascist
    'PDV_fa_c0_0': BUILD_CIV % 1 + '\n\t\t\tadd_war_support = 0.02',
    'PDV_fa_c0_2': 'add_tech_bonus = { name = cdw_pdv_autarky_research bonus = 0.5 uses = 1 category = industry }\n\t\t\tadd_stability = 0.02',
    'PDV_fa_c0_4': BUILD_MIL % 1,
    'PDV_fa_c0_6': BUILD_MIL % 2 + '\n\t\t\tadd_war_support = 0.03',
    'PDV_fa_c0_7': 'add_research_slot = 1\n\t\t\tadd_war_support = 0.03',
    'PDV_fa_c1_1': 'add_manpower = 25000\n\t\t\tadd_stability = 0.02',
    'PDV_fa_c1_3': 'add_manpower = 40000',
    'PDV_fa_c1_5': 'add_stability = 0.03\n\t\t\tadd_war_support = 0.02',
    'PDV_fa_c3_0': 'add_war_support = 0.04\n\t\t\tadd_command_power = 25',
    'PDV_fa_c3_2': 'add_command_power = 30\n\t\t\tadd_equipment_to_stockpile = { type = infantry_equipment amount = 1200 }',
    'PDV_fa_c3_4': 'add_stability = 0.03\n\t\t\tadd_command_power = 25',

    # ------------------------------------------------------------ monarchist
    'PDV_mo_c0_0': BUILD_CIV % 1 + '\n\t\t\tadd_stability = 0.02',
    'PDV_mo_c0_2': 'add_manpower = 20000\n\t\t\tadd_stability = 0.03',
    'PDV_mo_c0_4': BUILD_INFRA % 2,
    'PDV_mo_c0_6': 'add_tech_bonus = { name = cdw_pdv_court_research bonus = 0.5 uses = 1 category = industry }\n\t\t\tadd_political_power = 25',
    'PDV_mo_c0_7': 'add_stability = 0.05\n\t\t\tadd_political_power = 25',
    'PDV_mo_c1_1': 'add_manpower = 25000\n\t\t\tadd_stability = 0.02',
    'PDV_mo_c1_3': 'add_manpower = 20000\n\t\t\tadd_army_experience = 25',
    'PDV_mo_c1_5': 'add_tech_bonus = { name = cdw_pdv_academy_research bonus = 0.5 uses = 2 category = electronics }',
    'PDV_mo_c3_0': 'add_command_power = 30\n\t\t\tadd_political_power = 25',
    'PDV_mo_c3_2': 'add_war_support = 0.03\n\t\t\tadd_army_experience = 25',
    'PDV_mo_c3_4': 'add_command_power = 30\n\t\t\tadd_equipment_to_stockpile = { type = artillery_equipment amount = 300 }',
    'PDV_mo_c3_6': 'add_command_power = 30\n\t\t\tadd_political_power = 25',
    'PDV_mo_c3_7': 'add_war_support = 0.04\n\t\t\tadd_command_power = 50',

    # -------------------------------------------------------------- navy misc
    'PDV_nv_admiralty': 'add_navy_experience = 50\n\t\t\tadd_tech_bonus = { name = cdw_pdv_admiralty_research bonus = 0.5 uses = 1 category = cruiser }',

    # ------------------------------------------------- the four roads proper
    'PDV_cm_review': '''set_politics = { ruling_party = communism elections_allowed = no }
			add_popularity = { ideology = communism popularity = 0.10 }
			remove_ideas = PDV_purged_officer_corps
			add_ideas = PDV_officers_returning
			add_army_experience = 25''',
    'PDV_dm_review': '''set_politics = { ruling_party = democratic elections_allowed = yes }
			add_popularity = { ideology = democratic popularity = 0.15 }
			remove_ideas = PDV_purged_officer_corps
			add_ideas = PDV_officers_returning
			remove_ideas = PDV_hollow_army
			add_ideas = PDV_army_rebuilding
			add_stability = 0.03''',
    'PDV_fa_review': '''set_politics = { ruling_party = fascism elections_allowed = no }
			add_popularity = { ideology = fascism popularity = 0.15 }
			remove_ideas = PDV_purged_officer_corps
			add_ideas = PDV_officers_returning
			add_army_experience = 25''',
    'PDV_mo_review': '''set_politics = { ruling_party = neutrality elections_allowed = no }
			add_popularity = { ideology = neutrality popularity = 0.15 }
			remove_ideas = PDV_purged_officer_corps
			add_ideas = PDV_officers_returning
			add_political_power = 25''',
}

# extra effects bolted onto hub focuses (spine2 / spine4)
HUB_IDEAS = {
    'cm': {'spine2': 'PDV_state_plan', 'spine4': 'PDV_party_state'},
    'dm': {'spine2': 'PDV_republic_charter', 'spine4': 'PDV_open_society'},
    'fa': {'spine2': 'PDV_corporate_economy', 'spine4': 'PDV_reich_doctrine'},
    'mo': {'spine2': 'PDV_crown_restored', 'spine4': 'PDV_army_of_the_crown'},
}

# all Vyratia national spirits: id -> (picture, [(modifier, value), ...])
IDEAS = {
    'PDV_rebuilt_staff': ('generic_army_war_college',
                          [('army_org_factor', 0.05), ('experience_gain_army_factor', 0.10)]),
    'PDV_civil_war_scars': ('generic_build_infrastructure',
                            [('stability_factor', -0.15), ('industrial_capacity_factory', -0.15)]),
    'PDV_federal_republic': ('generic_foreign_capital',
                             [('stability_factor', 0.10), ('political_power_gain', 0.15),
                              ('industrial_capacity_factory', 0.10)]),
    'PDV_reich': ('generic_fascist_workers',
                  [('army_attack_factor', 0.05), ('war_support_factor', 0.10),
                   ('industrial_capacity_factory', 0.05)]),
    'PDV_leaderless': ('generic_morale_bonus',
                       [('army_org_factor', -0.20), ('army_morale_factor', -0.20),
                        ('political_power_gain', -0.25)]),
    'PDV_peoples_defence': ('generic_morale_bonus', [('army_defense_factor', 0.50)]),
    # Renderbosch is bought one masthead at a time: the drift is the point
    'PDV_rbd_infiltration': ('generic_propaganda',
                             [('neutrality_drift', 0.5), ('political_power_gain', 0.05)]),
    'PDV_crown_restored': ('generic_foreign_capital',
                           [('stability_factor', 0.05), ('political_power_gain', 0.10),
                            ('war_support_factor', 0.05)]),
    'PDV_state_plan': ('generic_production',
                       [('industrial_capacity_factory', 0.05), ('consumer_goods_factor', 0.05)]),
    'PDV_party_state': ('generic_propaganda',
                        [('stability_factor', 0.08), ('political_power_gain', 0.10)]),
    'PDV_republic_charter': ('generic_foreign_capital',
                             [('stability_factor', 0.08), ('research_speed_factor', 0.03)]),
    'PDV_open_society': ('generic_positive_trade_relations',
                         [('political_power_gain', 0.10), ('consumer_goods_factor', -0.03)]),
    'PDV_corporate_economy': ('generic_fascist_workers',
                              [('industrial_capacity_factory', 0.08), ('stability_factor', -0.03)]),
    'PDV_reich_doctrine': ('generic_military_sphere',
                           [('war_support_factor', 0.10), ('army_attack_factor', 0.05)]),
    'PDV_army_of_the_crown': ('generic_army_war_college',
                              [('army_defense_factor', 0.05), ('experience_gain_army_factor', 0.10)]),
}

NEW_IDEA_LOC = {
    'PDV_state_plan': ('The State Plan', 'The plan is not a forecast, it is an order with a number attached. Factories get targets they cannot argue with and the party gets an alibi.'),
    'PDV_party_state': ('The Party State', 'Every office in the country now has a party member standing beside it, and the party is no longer a faction inside the state - it is the state.'),
    'PDV_republic_charter': ('The Charter', 'A written constitution, a court that can void a law and a chamber that can be dissolved only by itself. It is the machine that makes the others obey.'),
    'PDV_open_society': ('An Open Society', 'Newspapers that print what they like, and a government that has learned it survives them. Liberty here is a policy with a budget line.'),
    'PDV_corporate_economy': ('The Corporate Economy', 'Industry, labour and the state are welded into one body that produces a great deal and complains very quietly.'),
    'PDV_reich_doctrine': ('The Reich Doctrine', 'The army is told it exists to expand the state, not to defend it - and the state is told the army is always right.'),
    'PDV_army_of_the_crown': ('The Royal Army', 'Small, slow, immaculately turned out, and loyal to a person rather than to a constitution.'),
}

# ---------------------------------------------------------------------------
# vanilla icons (every name must exist in Interface/goals.gfx)
# ---------------------------------------------------------------------------
ICON_RULES = [
    # ideology / political
    ('party reviews', 'GFX_goal_support_communism'),
    ('speech in the chamber', 'GFX_goal_support_democracy'),
    ('cells take root', 'GFX_goal_support_fascism'),
    ('letters to the court', 'GFX_goal_support_neutrality'),
    ('congress', 'GFX_goal_support_communism'),
    ('constitution', 'GFX_goal_generic_national_unity'),
    ('federal courts', 'GFX_goal_generic_national_unity'),
    ('federal settlement', 'GFX_goal_generic_alliance'),
    ('coup', 'GFX_goal_generic_dangerous_deal'),
    ('civil war', 'GFX_goal_generic_occupy_start_war'),
    ('reich reborn', 'GFX_goal_support_fascism'),
    ('vyratian reich', 'GFX_goal_panzerwaffe'),
    ('crown restored', 'GFX_goal_support_neutrality'),
    ('royal coup', 'GFX_goal_generic_dangerous_deal'),
    # industry / economy
    ('pits', 'GFX_goal_generic_construct_civ_factory'),
    ('five year plan', 'GFX_goal_generic_production'),
    ('steel', 'GFX_goal_generic_construct_mil_factory'),
    ('grain', 'GFX_goal_generic_consumer_goods'),
    ('corn laws', 'GFX_goal_generic_consumer_goods'),
    ('bank', 'GFX_goal_generic_production2'),
    ('rail', 'GFX_goal_generic_construct_infrastructure'),
    ('road', 'GFX_goal_reichsautobahn'),
    ('motorway', 'GFX_goal_reichsautobahn'),
    ('public works', 'GFX_goal_generic_construct_infrastructure'),
    ('heavy industry', 'GFX_goal_generic_construct_mil_factory'),
    ('industry', 'GFX_goal_generic_construct_mil_factory'),
    ('economy', 'GFX_goal_generic_production'),
    ('autarky', 'GFX_goal_generic_production'),
    ('estates', 'GFX_goal_generic_construct_civ_factory'),
    ('tenant', 'GFX_goal_generic_consumer_goods'),
    ('cooperative', 'GFX_goal_generic_positive_trade_relations'),
    ('tax', 'GFX_goal_generic_production2'),
    ('budget', 'GFX_goal_generic_production2'),
    ('plantation', 'GFX_goal_generic_consumer_goods'),
    ('merchant', 'GFX_goal_generic_trade'),
    ('guilds', 'GFX_goal_generic_production2'),
    ('arsenal', 'GFX_goal_generic_construct_mil_factory'),
    ('war economy', 'GFX_goal_generic_construct_mil_factory'),
    ('war economy plan', 'GFX_goal_generic_construct_mil_factory'),
    # society
    ('school', 'GFX_goal_generic_propaganda'),
    ('literacy', 'GFX_goal_generic_propaganda'),
    ('university', 'GFX_goal_generic_scientific_exchange'),
    ('academy', 'GFX_goal_generic_scientific_exchange'),
    ('press', 'GFX_goal_generic_propaganda'),
    ('clinic', 'GFX_goal_generic_positive_trade_relations'),
    ('health', 'GFX_goal_generic_positive_trade_relations'),
    ('housing', 'GFX_goal_generic_construction'),
    ('women', 'GFX_goal_generic_propaganda'),
    ('church', 'GFX_goal_support_neutrality'),
    ('charity', 'GFX_goal_generic_positive_trade_relations'),
    ('poor law', 'GFX_goal_generic_positive_trade_relations'),
    ('civic', 'GFX_goal_generic_national_unity'),
    ('fair', 'GFX_goal_generic_national_unity'),
    ('ceremonies', 'GFX_goal_support_neutrality'),
    ('community', 'GFX_goal_generic_national_unity'),
    ('society', 'GFX_goal_generic_national_unity'),
    ('new man', 'GFX_goal_generic_propaganda'),
    ('youth', 'GFX_goal_generic_propaganda'),
    ('mother and child', 'GFX_goal_generic_positive_trade_relations'),
    ('labour front', 'GFX_goal_generic_production2'),
    ('cadre', 'GFX_goal_generic_propaganda'),
    ('nobility', 'GFX_goal_support_neutrality'),
    ('guilds restored', 'GFX_goal_generic_production2'),
    # army
    ('division', 'GFX_goal_generic_army_doctrines'),
    ('regiment', 'GFX_goal_generic_army_doctrines'),
    ('household troops', 'GFX_goal_generic_army_doctrines'),
    ('guard', 'GFX_goal_generic_defence'),
    ('militia', 'GFX_goal_generic_small_arms'),
    ('officer', 'GFX_goal_generic_position_armies'),
    ('staff', 'GFX_goal_generic_position_armies'),
    ('war college', 'GFX_goal_generic_army_doctrines'),
    ('war academy', 'GFX_goal_generic_army_doctrines'),
    ('depot', 'GFX_goal_generic_small_arms'),
    ('fort', 'GFX_goal_generic_defence'),
    ('mobilisation', 'GFX_goal_generic_position_armies'),
    ('commissar', 'GFX_goal_generic_position_armies'),
    ('cavalry', 'GFX_goal_generic_cavalry'),
    ('tank', 'GFX_goal_generic_army_tanks'),
    ('armour', 'GFX_goal_generic_army_tanks'),
    ('barrels', 'GFX_goal_generic_build_tank'),
    ('hulls', 'GFX_goal_generic_build_tank'),
    ('artillery', 'GFX_goal_generic_army_artillery'),
    ('battery', 'GFX_goal_generic_army_artillery2'),
    ('counter-battery', 'GFX_goal_generic_army_artillery2'),
    ('gun', 'GFX_goal_generic_army_artillery'),
    ('fortress', 'GFX_goal_fortify_the_westwall'),
    ('columns', 'GFX_goal_generic_army_motorized'),
    ('combined arms', 'GFX_goal_generic_army_doctrines'),
    ('manual', 'GFX_goal_generic_army_doctrines'),
    ('doctrine for the army', 'GFX_goal_generic_army_doctrines'),
    ('total war', 'GFX_goal_generic_major_war'),
    ('reichswehr', 'GFX_goal_generic_military_sphere'),
    ('blackshirt', 'GFX_goal_generic_small_arms'),
    ('stormtroop', 'GFX_goal_generic_small_arms'),
    ('officer caste', 'GFX_goal_generic_position_armies'),
    ('officer families', 'GFX_goal_generic_position_armies'),
    ('reserve regiments', 'GFX_goal_generic_position_armies'),
    ('royal engineers', 'GFX_goal_generic_construction'),
    # air
    ('air arm', 'GFX_goal_generic_build_airforce'),
    ('fighter', 'GFX_goal_generic_air_fighter'),
    ('interceptor', 'GFX_goal_generic_air_fighter2'),
    ('bomber', 'GFX_goal_generic_air_bomber'),
    ('ground attack', 'GFX_goal_generic_CAS'),
    ('dive bomber', 'GFX_goal_generic_CAS'),
    ('strike wing', 'GFX_goal_generic_CAS'),
    ('radar', 'GFX_goal_generic_radar'),
    ('airfield', 'GFX_goal_generic_air_production'),
    ('air doctrine', 'GFX_goal_generic_air_doctrine'),
    ('air force', 'GFX_goal_generic_build_airforce'),
    ('air militia', 'GFX_goal_generic_air_fighter'),
    # navy
    ('yards', 'GFX_goal_generic_construct_naval_dockyard'),
    ('ships that are seen', 'GFX_goal_generic_navy_cruiser'),
    ('ships that are not', 'GFX_goal_generic_navy_submarine'),
    ('cruiser', 'GFX_goal_generic_navy_cruiser'),
    ('pens', 'GFX_goal_generic_navy_submarine'),
    ('destroyer', 'GFX_goal_generic_build_navy'),
    ('wolfpack', 'GFX_goal_generic_wolf_pack'),
    ('battle line', 'GFX_goal_generic_navy_battleship'),
    ('mine', 'GFX_goal_generic_navy_anti_submarine'),
    ('screen', 'GFX_goal_generic_navy_anti_submarine'),
    ('silent', 'GFX_goal_generic_navy_submarine'),
    ('naval doctrine', 'GFX_goal_generic_navy_doctrines_tactics'),
    ('coastal', 'GFX_goal_generic_defence'),
    ('marines', 'GFX_goal_generic_amphibious_assault'),
    ('convoy', 'GFX_goal_generic_trade'),
    ('trade war', 'GFX_goal_generic_navy_anti_submarine'),
    ('admiralty', 'GFX_goal_generic_build_navy'),
    ('naval academy', 'GFX_goal_generic_navy_doctrines_tactics'),
    ('fleet air', 'GFX_goal_generic_navy_carrier'),
    ('navy law', 'GFX_goal_generic_navy_battleship'),
    # diplomacy / territory
    ('embassy', 'GFX_goal_generic_improve_relations'),
    ('trade with', 'GFX_goal_generic_trade'),
    ('solidarity', 'GFX_goal_generic_alliance'),
    ('league', 'GFX_goal_generic_major_alliance'),
    ('anti-comintern', 'GFX_goal_anti_comintern_pact'),
    ('world revolution', 'GFX_goal_generic_major_war'),
    ('revolutionary diplomacy', 'GFX_goal_generic_alliance'),
    ('balkan', 'GFX_goal_generic_more_territorial_claims'),
    ('border', 'GFX_goal_generic_more_territorial_claims'),
    ('claim', 'GFX_goal_generic_demand_territory'),
    ('southern question', 'GFX_goal_generic_more_territorial_claims'),
    ('eastern marches', 'GFX_goal_generic_demand_territory'),
    ('protectorate', 'GFX_goal_generic_military_sphere'),
    ('infiltration', 'GFX_goal_generic_intelligence_exchange'),
    ('marriage', 'GFX_goal_generic_improve_relations'),
    ('envoy', 'GFX_goal_generic_improve_relations'),
    ('diplomatic corps', 'GFX_goal_generic_improve_relations'),
    ('old alliance', 'GFX_goal_generic_major_alliance'),
    ('renderbosch', 'GFX_goal_generic_demand_territory'),
    ('island', 'GFX_goal_generic_occupy_states_coastal'),
    ('neutral ground', 'GFX_goal_generic_neutrality_focus'),
    ('neighbourhood', 'GFX_goal_generic_improve_relations'),
    ('vyratian century', 'GFX_goal_generic_political_pressure'),
    ('cornish', 'GFX_goal_generic_alliance'),
    ('crown\'s reach', 'GFX_goal_generic_political_pressure'),
    ('organs', 'GFX_goal_generic_political_pressure'),
]

BRANCH_ICON = {'cm': 'GFX_goal_support_communism', 'dm': 'GFX_goal_support_democracy',
               'fa': 'GFX_goal_support_fascism', 'mo': 'GFX_goal_support_neutrality',
               'af': 'GFX_goal_generic_army_doctrines', 'nv': 'GFX_goal_generic_build_navy'}

ICON_BY_ID = {
    'PDV_the_directorate': 'GFX_goal_generic_political_pressure',
    'PDV_four_roads': 'GFX_goal_generic_national_unity',
    'PDV_af_root': 'GFX_goal_generic_army_doctrines',
    'PDV_af_capstone': 'GFX_goal_generic_build_airforce',
    'PDV_nv_root': 'GFX_goal_generic_construct_naval_dockyard',
    'PDV_nv_law': 'GFX_goal_generic_navy_battleship',
}
