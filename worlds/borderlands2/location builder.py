quest_loc_list = open("quest stuff.txt", "r").read()

def quest_loc_build(txt):
    split = txt.split("\n")
    MSQ_count = 0
    for line in split:
        line = line.removeprefix("    ")
        if not line.startswith("    "):
            print(f'''    "{line}": Borderlands2LocationData(in_game_region="Windshear Waste", story_region={MSQ_count}, type="Main Quest",),''')
            MSQ_count += 1
        else:
            line = line.lstrip("    ")
            print(f'''    "{line}": Borderlands2LocationData(in_game_region="Windshear Waste", story_region={MSQ_count}, type="Quest",),''')

#quest_loc_build(quest_loc_list)

def level_loc_build():
    start = 2
    level_stage = [4, 6, 8, 9, 10, 13, 14, 15, 17, 20, 21, 23, 27, 28, 29, 30, 31]
    for i in range(2, 81):
        if i in level_stage:
            start += 1
        if 61>= i >= 51:
            print(    f'''    "Level {i}": Borderlands2LocationData(in_game_region="Player", story_region={start}, type="Level", dlc=["UVHM 1"]),''')
            continue
        if 72 >= i > 61:
            print(f'''    "Level {i}": Borderlands2LocationData(in_game_region="Player", story_region={start}, type="Level", dlc=["UVHM 1", "UVHM 2"]),''')
            continue
        if i > 72:
            print(f'''    "Level {i}": Borderlands2LocationData(in_game_region="Player", story_region={start}, type="Level", dlc=["UVHM 1", "UVHM 2", "Fight for Sanctuary"]),''')
            continue
        print(f'''    "Level {i}": Borderlands2LocationData(in_game_region="Player", story_region={start}, type="Level",),''')

#level_loc_build()

def chara_skill_build():
    chara = [("Axton", ['Sentry', 'Ready', 'Laser Sight', 'Willing', 'Onslaught', 'Able', 'Scorched Earth', 'Grenadier', 'Crisis Management', 'Double Up', 'Impact', 'Expertise', 'Overload', 'Metal Storm', 'Steady', 'Battlefront', 'Longbow Turret', 'Duty Calls', 'Do or Die', 'Ranger', 'Nuke', 'Healthy', 'Preparation', 'Last Ditch Effort', 'Pressure', 'Forbearance', 'Quick Charge', 'Phalanx Shield', 'Resourceful', 'Mag-Lock', 'Grit', 'Gemini']),
             ("Maya", ['Ward', 'Accelerate', 'Suspension', 'Kinetic Reflection', 'Fleet', 'Inertia', 'Converge', 'Quicken', 'Sub-Sequence', 'Thoughtlock', "Mind's Eye", 'Sweet Release', 'Restoration', 'Wreck', 'Elated', 'Recompense', 'Res', 'Sustenance', 'Life Tap', 'Scorn', 'Flicker', 'Foresight', 'Immolate', 'Helios', 'Chain Reaction', 'Backdraft', 'Cloud Kill', 'Reaper', 'Blight Phoenix', 'Ruin']),
             ("Salvador", ['Locked and Loaded', 'Quick Draw', "I'm Your Huckleberry", 'All I Need is One', 'Divergent Likeness', 'Money Shot', 'Auto-Loader', 'Lay Waste', 'Down Not Out', 'Keep It Piping Hot', 'No Kill Like Overkill', 'Inconceivable', 'Filled to the Brim', 'All in the Reflexes', 'Last Longer', "I'm Ready Already", '5 Shots or 6', 'Steady as She Goes', 'Yippee Ki Yay', 'Double Your Fun', 'Get Some', 'Keep Firing...', 'Hard to Kill', 'Incite', 'Asbestos', "I'm the Juggernaut", "Ain't Got Time to Bleed", 'Out of Bubblegum', 'Fistful of Hurt', "Bus That Can't Slow Down", 'Just Got Real', 'Sexual Tyrannosaurus', 'Come At Me Bro']),
             ("Zero", ['Headsh0t', '0ptics', 'Killer', 'Precisi0n', '0ne Sh0t 0ne Kill', 'Vel0city', 'B0re', 'Kill C0nfirmed', 'At 0ne with the Gun', 'Critical Ascensi0n', 'Fast Hands', 'C0unter Strike', 'Fearless', 'Ambush', 'Rising Sh0t', 'Unf0rseen', 'Deathmark', 'Innervate', 'Tw0 Fang', 'Death Bl0ss0m', 'Killing Bl0w', 'Ir0n Hand', 'Grim', 'Be Like Water', 'F0ll0wthr0ugh', 'Backstab', 'Execute', 'Resurgence', 'Like The Wind', 'Many Must Fall']),
             ("Gaige", ['Close Enough', 'Cooking Up Trouble', 'Fancy Mathematics', 'Buck Up', 'The Better Half', 'Potent as a Pony', 'Upshot Robot', 'Unstoppable Force', 'Explosive Clap', 'Made of Sterner Stuff', '20% Cooler', 'Sharing is Caring', 'More Pep', 'Myelin', 'Shock Storm', 'The Stare', 'Strength of Five Gorillas', 'Electrical Burn', 'Shock and "AAAGGGGHHH!"', 'Evil Enchantress', 'One Two Boom', "Wires Don't Talk", 'Interspersed Outburst', 'Make it Sparkle', 'Smaller, Lighter, Faster', 'Anarchy', 'Preshrunk Cyberpunk', 'Robot Rampage', 'Blood Soaked Shields', 'Annoyed Android', 'Discord', 'Typecast Iconoclast', 'Rational Anarchist', 'Death From Above', 'The Nth Degree', 'With Claws']),
             ("Krieg", ['Blood Twitch', 'Blood-Filled Guns', 'Blood Overdrive', 'Bloody Revival', 'Taste of Blood', 'Blood Bath', 'Buzz Axe Bombardier', 'Fuel the Blood', 'Boiling Blood', 'Blood Trance', 'Nervous Blood', 'Bloodsplosion', 'Empty the Rage', 'Pull the Pin', 'Feed the Meat', 'Fuel the Rampage', 'Embrace the Pain', 'Thrill of the Kill', 'Light the Fuse', 'Strip the Flesh', 'Redeem the Soul', 'Salt the Wound', 'Silence the Voices', 'Release the Beast', 'Burn, Baby, Burn', 'Fuel the Fire', 'Pain is Power', 'Numbed Nerves', 'Elemental Elation', 'Delusional Damage', 'Fire Fiend', 'Hellfire Halitosis', 'Flame Flare', 'Elemental Empathy', 'Raving Retribution'])]
    for char, skills in chara:
        for skill in skills:
            print(f""""{skill}": Borderlands2ItemData(type="Skill", i_class=IC.progression, count=5, character="{char}"),""")

#chara_skill_build()

from Locations import optional_mission_list

def optional_item_build():
    for mission in optional_mission_list:
        print(f"""  "{mission} Unlock": Borderlands2ItemData(type="Optional Mission", i_class=IC.progression),""")

#optional_item_build()
