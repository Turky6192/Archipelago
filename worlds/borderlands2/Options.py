import typing

from Options import Toggle, Range, Choice, DeathLink, OptionSet, PerGameCommonOptions, OptionGroup, Removed, DefaultOnToggle
from dataclasses import dataclass

from .Locations import dlc_names


class Character(Choice):
    """
	Choose what character to play as. Choosing 'Any' will let you decide in-game.

	*Choosing Gaige or Krieg will require you to have the relevant DLC/Handsome Collection*
	"""
    display_name = "Player Character"
    option_Any = 0
    option_Salvador = 1
    option_Zer0 = 2
    option_Maya = 3
    option_Axton = 4
    option_Gaige = 5
    option_Krieg = 6
    default = 0


class Goal(Choice):
    """
	Sets the victory condition.

	- **Main Story:** Work your way through the base game Story Missions to defeat Handsome Jack and The Warrior.
	- **Boss Hunt:** Defeat a set number of Bosses.
	- **Claptrap's Quest:** Truly complete the "Claptrap's Secret Stash" mission by finding all the items (MacGuffins) he requests.
	"""
    display_name = "Goal"
    option_main_story = 0
    option_claptraps_quest = 1
    #option_boss_hunt = 2
    default = 0


class AllowedDLC(OptionSet):
    """
    Select which(if any) DLC's you want included into randomization.

    *All options are included by default.*
    """
    display_name = "Allowed DLC"
    valid_keys = [dlc for dlc in dlc_names]
    default = [dlc for dlc in dlc_names]


class MaxLevel(Range):
    """
	Sets the maximum level that logic will expect you to achieve.

	**Warning:** Levels above 50 require DLC and considerably more time to potentially reach.
	"""
    display_name = "Max Level"
    range_start = 30
    range_end = 80
    default = 36


class OptionalMissionLocking(Choice):
    """
    Optional Missions can be locked to delineate your playthrough more, or not to help speed up playthrough time.

    **Vanilla**: Optional Missions behave like normal, unlocking when the required prerequisite Story, or Optional,
                 Mission(s) are complete.
    **Grouped**: "Unlock" items give access to groupings of Optional Missions, grouped either by the starting NPC,
                 questline, narrative timing, or general location.
    **Full**: All Optional Missions have their own "Unlock" item, while also still requiring proper prerequisite access.

    *Note: "Full" may be forced to "Grouped" depending on other settings to maintain item/location balance.*
    """
    display_name = "Optional Mission Locking"
    option_vanilla = 0
    option_grouped = 1
    option_full = 2
    default = 1

class BossHuntCount(Range):
    """
	Sets the amount of Bosses you need to kill to goal.

	*Only relevant if "Boss Hunt" is your selected goal.*
	"""
    display_name = "Boss Hunt Count"
    range_start = 5
    range_end = 70  # Unsure of total bosses
    default = 25


class ClaptrapCount(Range):
    """
    Claptrap's Secret Stash mission requires you to find "The Corpse of Ug-Thak, Lord of Skags",
    "The Lost Staff of Mount Schuler", "The Head of The Destroyer of Worlds", "Default Dance Emote",
    and a certain amount of "Brown Rock"s, as determined by this option.
    """
    display_name = "Brown Rocks Required"
    range_start = 2
    range_end = 50  # Unsure how more ridiculous this could be
    default = 14


class SkillRandom(Choice):
    """Determines how, or if, your skills are randomized.

	- **Vanilla:** You receive a skill point on level up and can use it as normal.
	- **Points in Pool:** No longer receive skill points on level up, will instead receive them as items up to an
	    amount determined by your "Max Level" and "Extra Points" options.
	- **Skills in Pool:** Only usable if a specific character is set in your options. Adds a random selection
	    of your character's skills as items up to an amount determined by your "Max Level" and "Extra Points" options.
	"""
    display_name = "Skill Randomization"
    option_vanilla = 0
    option_points_in_pool = 1
    option_skills_in_pool = 2
    default = 1


class ExtraSkill(Range):
    """
	Adds extra skills or skill points to the pool

	*Will still add points to the pool if Skill Randomization is set to Vanilla.*
	"""
    display_name = "Extra Skills/Points"
    range_start = 0
    range_end = 40
    default = 0

# Maya max 126
# Axton max 128
# Zer0 max 126
# Salvador max 133
# Gaige max 127
# Krieg max 139


class BadassLevel(DefaultOnToggle):
    """Determines if Badass Levels are allowed or forced to be disabled."""
    display_name = "Allow Badass Levels"


class Chestsanity(Toggle):
    """
	Gives every interactable chest-like object a check that will be sent upon the first time opening it.

	**Warning:** There are A LOT of chests in this game, this will add a lot of filler to the item pool.
	"""
    display_name = "Chestsanity"


class Doorsanity(Toggle):
    """
    Locks access to every area that requires an interaction with a key named "{area} Key"
    """
    display_name = "Doorsanity"


class ExcludeTerramorphous(DefaultOnToggle):
    """
    Prevents progression being placed on the "Kill Terramorphous", "You. Will. Die. (Seriously.)",
    and the 2 Cult Symbol locations in Terramophous Peak.
    """
    display_name = "Exclude Terramorphous"


@dataclass
class Borderlands2Options(PerGameCommonOptions):
    character: Character
    goal: Goal
    allowed_dlc: AllowedDLC
    boss_hunt_count: BossHuntCount
    claptrap_count: ClaptrapCount
    optional_mission_locking: OptionalMissionLocking
    skill_randomization: SkillRandom
    extra_skills: ExtraSkill
    badass_level: BadassLevel
    max_level: MaxLevel
    chestsanity: Chestsanity
    doorsanity: Doorsanity
    exclude_terramorphous: ExcludeTerramorphous