from .Locations import location_data_table


meet_claptrap = [name for name, data in location_data_table.items() if data.story_region == 0]
pre_knuckle_dragger = [name for name, data in location_data_table.items() if data.story_region == 1]
meet_hammerlock = [name for name, data in location_data_table.items() if data.story_region == 2]
pre_flynt = [name for name, data in location_data_table.items() if data.story_region == 3]
pre_sanctuary = [name for name, data in location_data_table.items() if data.story_region == 4]
pre_plan_b = [name for name, data in location_data_table.items() if data.story_region == 5]
meet_lilith = [name for name, data in location_data_table.items() if data.story_region == 6]
meet_roland = [name for name, data in location_data_table.items() if data.story_region == 7]
pre_wilhelm = [name for name, data in location_data_table.items() if data.story_region == 8]
raise_sanctuary = [name for name, data in location_data_table.items() if data.story_region == 9]
find_sanctuary = [name for name, data in location_data_table.items() if data.story_region == 10]
pre_bloodwing = [name for name, data in location_data_table.items() if data.story_region == 11]
meet_brick = [name for name, data in location_data_table.items() if data.story_region == 12]
pre_opportunity = [name for name, data in location_data_table.items() if data.story_region == 13]
meet_angel = [name for name, data in location_data_table.items() if data.story_region == 14]
rolands_death = [name for name, data in location_data_table.items() if data.story_region == 15]
pre_arid_nexus = [name for name, data in location_data_table.items() if data.story_region == 16]
pre_fyrestone = [name for name, data in location_data_table.items() if data.story_region == 17]
meet_the_warrior = [name for name, data in location_data_table.items() if data.story_region == 18]
post_jack = [name for name, data in location_data_table.items() if data.story_region == 19]

story_regions = [meet_claptrap, pre_knuckle_dragger, meet_hammerlock, pre_flynt, pre_sanctuary, pre_plan_b, meet_lilith,
                 meet_roland, pre_wilhelm, raise_sanctuary, find_sanctuary, pre_bloodwing, meet_brick, pre_opportunity,
                 meet_angel, rolands_death, pre_arid_nexus, pre_fyrestone, meet_the_warrior, post_jack]

arid_nexus_badlands = [name for name, data in location_data_table.items() if data.in_game_region == "Arid Nexus Badlands"]
arid_nexus_boneyard = [name for name, data in location_data_table.items() if data.in_game_region == "Arid Nexus Boneyard"]
bloodshot_ramparts = [name for name, data in location_data_table.items() if data.in_game_region == "Bloodshot Ramparts"]
bloodshot_stronghold = [name for name, data in location_data_table.items() if data.in_game_region == "Bloodshot Stronghold"]
the_bunker = [name for name, data in location_data_table.items() if data.in_game_region == "The Bunker"]
caustic_caverns = [name for name, data in location_data_table.items() if data.in_game_region == "Caustic Caverns"]
control_core_angel = [name for name, data in location_data_table.items() if data.in_game_region == "Control Core Angel"]
the_dust = [name for name, data in location_data_table.items() if data.in_game_region == "The Dust"]
end_of_the_line = [name for name, data in location_data_table.items() if data.in_game_region == "End of the Line"]
eridium_blight = [name for name, data in location_data_table.items() if data.in_game_region == "Eridium Blight"]
finks_slaughterhouse = [name for name, data in location_data_table.items() if data.in_game_region == "Fink's Slaughterhouse"]
friendship_gulag = [name for name, data in location_data_table.items() if data.in_game_region == "Friendship Gulag"]
frostburn_canyon = [name for name, data in location_data_table.items() if data.in_game_region == "Frostburn Canyon"]
heros_pass = [name for name, data in location_data_table.items() if data.in_game_region == "Hero's Pass"]
lynchwood = [name for name, data in location_data_table.items() if data.in_game_region == "Lynchwood"]
natural_selection_annex = [name for name, data in location_data_table.items() if data.in_game_region == "Natural Selection Annex"]
opportunity = [name for name, data in location_data_table.items() if data.in_game_region == "Opportunity"]
ore_chasm = [name for name, data in location_data_table.items() if data.in_game_region == "Ore Chasm"]
sanctuary = [name for name, data in location_data_table.items() if data.in_game_region == "Sanctuary"]
sanctuary_hole = [name for name, data in location_data_table.items() if data.in_game_region == "Sanctuary Hole"]
sawtooth_cauldron = [name for name, data in location_data_table.items() if data.in_game_region == "Sawtooth Cauldron"]
southern_shelf = [name for name, data in location_data_table.items() if data.in_game_region == "Southern Shelf"]
southern_shelf_bay = [name for name, data in location_data_table.items() if data.in_game_region == "Southern Shelf Bay"]
southpaw_steam_and_power = [name for name, data in location_data_table.items() if data.in_game_region == "Southpaw Steam and Power"]
terramorphous_peak = [name for name, data in location_data_table.items() if data.in_game_region == "Terramorphous Peak"]
the_fridge = [name for name, data in location_data_table.items() if data.in_game_region == "The Fridge"]
the_highlands = [name for name, data in location_data_table.items() if data.in_game_region == "The Highlands"]
the_highlands_outwash = [name for name, data in location_data_table.items() if data.in_game_region == "The Highlands Outwash"]
the_holy_spirits = [name for name, data in location_data_table.items() if data.in_game_region == "The Holy Spirits"]
thousand_cuts = [name for name, data in location_data_table.items() if data.in_game_region == "Thousand Cuts"]
three_horns_divide = [name for name, data in location_data_table.items() if data.in_game_region == "Three Horns Divide"]
three_horns_valley = [name for name, data in location_data_table.items() if data.in_game_region == "Three Horns Valley"]
tundra_express = [name for name, data in location_data_table.items() if data.in_game_region == "Tundra Express"]
vault_of_the_warrior = [name for name, data in location_data_table.items() if data.in_game_region == "Vault of The Warrior"]
wildlife_exploitation_preserve = [name for name, data in location_data_table.items() if data.in_game_region == "Willife Exploitation Preserve"]
windshear_waste = [name for name, data in location_data_table.items() if data.in_game_region == "Windshear Waste"]

in_game_regions = [arid_nexus_badlands, arid_nexus_boneyard, bloodshot_ramparts, bloodshot_stronghold, the_bunker,
                   caustic_caverns, control_core_angel, the_dust, end_of_the_line, eridium_blight, finks_slaughterhouse,
                   friendship_gulag, frostburn_canyon, heros_pass, lynchwood, natural_selection_annex, opportunity,
                   ore_chasm, sanctuary, sanctuary_hole, sawtooth_cauldron, southern_shelf, southern_shelf_bay,
                   southpaw_steam_and_power, terramorphous_peak, the_fridge, the_highlands, the_highlands_outwash,
                   the_holy_spirits, thousand_cuts, three_horns_divide, three_horns_valley, tundra_express,
                   vault_of_the_warrior, wildlife_exploitation_preserve, windshear_waste]