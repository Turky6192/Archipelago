from __future__ import annotations

import logging
from typing import List, Dict, Any

from Options import OptionError
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, LocationProgressType
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, forbid_item, add_rule

from .Items import *
from .Locations import *
from .Options import Borderlands2Options
from .Regions import *
from .Rules import *


class Borderlands2Web(WebWorld):
    theme = "ice"
    rich_text_options_doc = True

class Borderlands2World(World):
    game = "Borderlands 2"
    web = Borderlands2Web()
    options: Borderlands2Options
    options_dataclass = Borderlands2Options
    item_name_to_id = item_table
    location_name_to_id = location_table

    selected_dlc: List[str] = []
    origin_region_name = "Player"
    pooled_skills: int
    max_level: int
    chosen_char: int
    excluded_opt_missions: List[str] = []

    player_location_pool: Dict[str, int]

    def generate_early(self) -> None:
        # Verify a specific character is chosen if skill rando is set to "skills in pool"
        self.pooled_skills = self.options.extra_skills.value
        self.chosen_char = self.options.character.value
        self.max_level = self.options.max_level.value
        if self.options.skill_randomization.value > 0:
            self.pooled_skills += self.max_level - 3
        if self.chosen_char == 0 and self.options.skill_randomization.value == 2:
            logging.warning("Borderlands 2: Player %s (%s has Skill Randomization set to "
                              "'Skills in Pool' but did not select a specific character. Using 'Points in Pool instead.",
                            self.player, self.player_name)

        # Verify that the player can reach all level locations wanted with chosen DLC options
        selected_dlc = list(self.options.allowed_dlc)
        if self.max_level > 50:
            level_dlc =  {"UVHM 1": 11, "UVHM 2": 11, "Fight for Sanctuary": 8}
            allowed_max = 50 + sum(level_dlc[dlc] for dlc in level_dlc if dlc in selected_dlc)
            if allowed_max < self.max_level:
                raise OptionError(f"Borderlands 2: Player {self.player} ({self.player_name} does not have required DLCs"
                                  f" enabled to reach desired Max Level ({self.max_level}).)")

    def create_regions(self) -> None:
        # Current just use this for the level removal
        self.player_location_pool = self.location_name_to_id.copy()

        # Removes levels from location pool above selected max level
        if self.max_level < 80:
            for level in range(self.max_level + 1, 81):
                del self.player_location_pool[f"Level {level}"]
        # "Visit" locations are just for doorsanity
        if self.options.doorsanity == 0:
            for location in region_visit_list:
                del self.player_location_pool[location]

        # Making the regions
        for region_name in in_game_regions_map.keys():
            region = Region(region_name, self.player, self.multiworld)
            mapped_loc_per_region = {name: id for name, id in self.player_location_pool.items() if name in in_game_region_loc_map[region_name]}
            region.add_locations(mapped_loc_per_region)
            terra_locs = [name for name, data in location_data_table.items() if data.in_game_region == "Terramorphous Peak"]
            # Might as well alter the locations needed, while adding them to each main region
            for location in region.get_locations():
                # Add proper "Progressive Story Mission" requirements
                prog_required = location_data_table[location.name].story_region
                if 19 > prog_required > 0:
                    location.access_rule = lambda state, req=prog_required: state.has("Progressive Story Mission", self.player, req)
                if prog_required == 19:
                    location.access_rule = lambda state: state.has("Progressive Story Mission", self.player, 18)
                # Add the Unlock items for Optional Missions
                if location.name in optional_mission_list:
                    add_rule(location, lambda state, name=location.name: state.has(f"{name} Unlock", self.player))
                    forbid_item(self.multiworld.get_location(location.name, self.player), f"{location.name} Unlock", self.player)
                # Exclude Terramorphous
                if  self.options.exclude_terramorphous == 1 and location.name in terra_locs:
                    location.progress_type = LocationProgressType.EXCLUDED
                # Give bosses that require an Optional Mission to access the proper requirements
                if location.name.startswith("Kill ") and location.name != "Kill Yourself":
                    boss_reqs = next((data.prereq_mission for name, data in location_data_table.items() if name == location.name), None)
                    if boss_reqs:
                        add_rule(location, lambda state, name=boss_reqs: state.can_reach(self.multiworld.get_location(f"{name}", self.player)))
                # Set door-sanity logic and forbid Keys from being put in the region they unlock
                if self.options.doorsanity == 1:
                    forbid_item(self.multiworld.get_location(location.name, self.player), f"{region_name} Key", self.player)

            # Finally add the region to the world
            self.multiworld.regions.append(region)

        # Once all regions and their locations are added we can want to ensure no mission unlocks are self-locking
        for location in self.get_locations():
            if location.name in optionals_w_dependants.keys():
                add_locks = recur_opt_key_lock(location.name, optionals_w_dependants)
                for prereq in add_locks:
                    if prereq:
                        forbid_item(self.multiworld.get_location(prereq, self.player), f"{location.name} Unlock", self.player)
            if location.name in optionals_w_prereq.keys():
                prereq_locks = recur_opt_key_lock(location.name, optionals_w_prereq)
                for prereq in prereq_locks:
                    add_rule(location, lambda state, name=prereq: state.has(f"{name} Unlock", self.player))


        # Connecting the regions and give key requirements
        for region_name, exits in in_game_regions_map.items():
            region = self.get_region(region_name)
            if self.options.doorsanity == 1 and region_name != "Player":
                for exit in exits:
                    region.connect(self.get_region(exit), f"{region_name} to {exit}", lambda state, key=exit: state.has(f"{key} Key", self.player))
            else:
                region.add_exits(exits)

        # Victory conditions
        if self.options.goal == 0:
            jack_region = self.get_region("Vault of the Warrior")
            jack_region.locations.append(Borderlands2Location(self.player, "Kill Jack", None, jack_region))
            self.multiworld.get_location("Kill Jack", self.player).place_locked_item(self.create_event("Victory"))
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
            set_rule(self.multiworld.get_location("Kill Jack", self.player), lambda state: state.has("Progressive Story Mission", self.player, 18))
        elif self.options.goal == 1:
            claptrap_region = self.get_region("Player")
            claptrap_region.locations.append(Borderlands2Location(self.player, "Completed Claptrap's Quest", None, claptrap_region))
            self.multiworld.get_location("Completed Claptrap's Quest", self.player).place_locked_item(self.create_event("Victory"))
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
            set_rule(self.multiworld.get_location("Completed Claptrap's Quest", self.player),
                     lambda state: state.has_from_list(claptrap_items, self.player, 4 + self.options.claptrap_count))

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Player", self.player), "my_world.puml")

    def create_item(self, name: str) -> Borderlands2Item:
        item_data = item_data_table[name]
        item_class = item_data.i_class
        return Borderlands2Item(name, item_class, self.item_name_to_id[name], self.player)

    def create_event(self, event: str) -> Borderlands2Item:
        return Borderlands2Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        borderlands2_items: List[Borderlands2Item] = []
        # Story missions are the main bottleneck so they always need added
        borderlands2_items +=[self.create_item("Progressive Story Mission") for _ in range(18)]
        self.multiworld.early_items[self.player]["Progressive Story Mission"] = 1
        if self.options.doorsanity == 1:
            self.multiworld.early_items[self.player]["Southern Shelf Key"] = 1

        # mw_games = [game.game for game in self.multiworld.worlds.values()]
        # if not "Borderlands 2" in mw_games:
        #     borderlands2_items += [self.create_item("Progressive Story Mission") for _ in range(17)]
        #
        # else:
        #     if self.options.doorsanity == 1:
        #         for region in story_region_names[1:10]:
        #             item = self.create_item("Progressive Story Mission")
        #             while story_region_names.index(region) == 1:
        #                 location = self.random.choice(self.get_region(region).get_locations())
        #                 while location.item != None:
        #                     location = self.random.choice(self.get_region(region).get_locations())
        #                 self.multiworld.get_location(location.name, self.player).place_locked_item(item)
        #                 break
        #             while story_region_names.index(region) > 1:
        #                 location = self.random.choice(self.get_region(region).get_locations())
        #                 second = self.random.choice(self.get_region(region).get_locations())
        #                 while location.name == second.name or second.item != None:
        #                     second = self.random.choice(self.get_region(region).get_locations())
        #                 second_item = ""
        #                 potential_keys = [name for name, lowest_access in in_game_progress_map.items() if lowest_access < story_region_names.index(region)]
        #                 second_item = self.create_item(f"{self.random.choice(potential_keys)} Key")
        #                 self.multiworld.get_location(location.name, self.player).place_locked_item(item)
        #                 self.multiworld.get_location(second.name, self.player).place_locked_item(second_item)
        #                 break
        #     else:
        #         for region in story_region_names[1:18]:
        #             location = self.random.choice(self.get_region(region).get_locations())
        #             item = self.create_item("Progressive Story Mission")
        #             self.multiworld.get_location(location.name, self.player).place_locked_item(item)


        # Adding Claptrap items, our MacGuffin goal items
        if self.options.goal == 1:
            for item in claptrap_items:
                if item == "Brown Rock":
                    borderlands2_items += [self.create_item(item) for _ in range(self.options.claptrap_count)]
                else:
                    borderlands2_items.append(self.create_item(item))


        # Doorsanity keys
        if self.options.doorsanity == 1:
            for key, data in item_data_table.items():
                if data.type == "Region Key":
                    borderlands2_items.append(self.create_item(key))

        # To set up the pool of skills for the player's selected character
        def get_skills(character, num) -> List[str]:
            characters = {1: "Salvador", 2: "Zero", 3: "Maya", 4: "Axton", 5: "Gaige", 6: "Krieg"}
            skills: List[str] = []
            chosen = []
            for skill, data in item_data_table.items():
                if data.character == characters[character]:
                    for _ in range(data.count):
                        skills.append(skill)
            self.random.shuffle(skills)
            for _ in range(num):
                chosen.append(skills.pop())
            return chosen

        # Skill points or character-specific skills next
        if self.chosen_char == 0 or self.chosen_char > 0 and self.options.skill_randomization.value < 2:
            borderlands2_items += [self.create_item("Skill Point") for _ in range(self.pooled_skills)]
        elif self.chosen_char > 0 and self.options.skill_randomization.value == 2:
            skills = get_skills(self.chosen_char, max(self.pooled_skills + 5, 50)) # Add a few extra to help synergy
            for skill in skills:
                skill_item = self.create_item(skill)
                borderlands2_items.append(skill_item)

        # Create keys for Optional Missions
        for item in optional_mission_items:
            opt_mission_item = self.create_item(item)
            borderlands2_items.append(opt_mission_item)

        # Filler for remaining locations
        self.multiworld.itempool += borderlands2_items
        remaining_locs = len(self.multiworld.get_unfilled_locations(self.player)) - len(borderlands2_items)
        for _ in range(remaining_locs):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))



    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    #def set_rules(self) -> None:
    #     """Method for setting the rules on the World's regions and locations."""

        # region_count = 0
        # region_index_list: Dict[str, int] = {}
        # for region in story_region_names:
        #     region_index_list[region] = region_count
        #     region_count += 1
        #
        # for region_name in story_region_names:
        #     if 19 > region_index_list[region_name] > 4 and self.options.skill_randomization.value > 0:
        #         set_rule(self.get_entrance(f"Story Progress {region_index_list[region_name] + 1}"),
        #                  lambda state, value=min(region_index_list[region_name], 18): state.has(
        #                      "Progressive Story Mission", self.player, value) and
        #                  state.has_from_list(skill_items, self.player, int(value * 1.8 - 5)))
        #     elif region_index_list[region_name] < 19:
        #         set_rule(self.get_entrance(f"Story Progress {region_index_list[region_name] + 1}"),
        #                  lambda state, value=min(region_index_list[region_name], 18):
        #                  state.has("Progressive Story Mission", self.player, value))
        #
        # for region, story_progress in in_game_progress_map.items():
        #     self.multiworld.register_indirect_condition(self.get_region(f"{region}"),self.get_entrance(f"Story Progress {story_progress}"))

    # def pre_fill(self) -> None:




    #
    # def connect_entrances(self) -> None:
    #     """Method to finalize the source and target regions of the World's entrances"""
    #     pass
    #
    # def generate_basic(self) -> None:
    #     """
    #     Useful for randomizing things that don't affect logic but are better to be determined before the output stage.
    #     i.e. checking what the player has marked as priority or randomizing enemies
    #     """
    #     pass
    #
    # def fill_hook(self,
    #               progitempool: List["Item"],
    #               usefulitempool: List["Item"],
    #               filleritempool: List["Item"],
    #               fill_locations: List["Location"]) -> None:
    #     """Special method that gets called as part of distribute_items_restrictive (main fill)."""
    #     pass
    #
    # def post_fill(self) -> None:
    #     """
    #     Optional Method that is called after regular fill. Can be used to do adjustments before output generation.
    #     This happens before progression balancing, so the items may not be in their final locations yet.
    #     """
    #
    # def generate_output(self, output_directory: str) -> None:
    #     """
    #     This method gets called from a threadpool, do not use multiworld.random here.
    #     If you need any last-second randomization, use self.random instead.
    #     """
    #     pass
    #
    def fill_slot_data(self) -> Dict[str, Any]:  # json of WebHostLib.models.Slot
        slot_data: Dict[str, Any] = {
            "character": self.options.character,
            "allowed_dlc": self.options.allowed_dlc,
            "max_level": self.max_level,
            "skill_randomization": self.options.skill_randomization,
            "goal": self.options.goal,
            "claptrap_count": self.options.claptrap_count,
            "doorsanity": self.options.doorsanity,
            "badass_level": self.options.badass_level,
            "chestsanity": self.options.chestsanity,
        }

        return slot_data

    #
    # def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
    #     """
    #     Fill in additional entrance information text into locations, which is displayed when hinted.
    #     structure is {player_id: {location_id: text}} You will need to insert your own player_id.
    #     """
    #     pass
    #
    # def modify_multidata(self, multidata: Dict[str, Any]) -> None:
    #     """For deeper modification of server multidata."""
    #     pass
    #
    # # Spoiler writing is optional, these may not get called.
    # def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
    #     """
    #     Write to the spoiler header. If individual it's right at the end of that player's options,
    #     if as stage it's right under the common header before per-player options.
    #     """
    #     pass
    #
    # def write_spoiler(self, spoiler_handle: TextIO) -> None:
    #     """
    #     Write to the spoiler "middle", this is after the per-player options and before locations,
    #     meant for useful or interesting info.
    #     """
    #     pass
    #
    # def write_spoiler_end(self, spoiler_handle: TextIO) -> None:
    #     """Write to the end of the spoiler"""
    #     pass
    #
    # # end of ordered Main.py calls
    #
    #
    #
    # @classmethod
    # def create_group(cls, multiworld: "MultiWorld", new_player_id: int, players: Set[int]) -> World:
    #     """
    #     Creates a group, which is an instance of World that is responsible for multiple others.
    #     An example case is ItemLinks creating these.
    #     """
    #     for option_key, option in cls.options_dataclass.type_hints.items():
    #         getattr(multiworld, option_key)[new_player_id] = option.from_any(option.default)
    #     group = cls(multiworld, new_player_id)
    #     group.options = cls.options_dataclass(**{option_key: option.from_any(option.default)
    #                                              for option_key, option in cls.options_dataclass.type_hints.items()})
    #     group.options.accessibility = ItemsAccessibility(ItemsAccessibility.option_items)
    #
    #     return group
    #
    # # decent place to implement progressive items, in most cases can stay as-is
    # def collect_item(self, state: "CollectionState", item: "Item", remove: bool = False) -> Optional[str]:
    #     """
    #     Collect an item name into state. For speed reasons items that aren't logically useful get skipped.
    #     Collect None to skip item.
    #     :param state: CollectionState to collect into
    #     :param item: Item to decide on if it should be collected into state
    #     :param remove: indicate if this is meant to remove from state instead of adding.
    #     """
    #     if item.advancement:
    #         return item.name
    #     return None
    #
    # def get_pre_fill_items(self) -> List["Item"]:
    #     """
    #     Used to return items that need to be collected when creating a fresh all_state, but don't exist in the
    #     multiworld itempool.
    #     """
    #     return []
    #
    # # these two methods can be extended for pseudo-items on state
    # def collect(self, state: "CollectionState", item: "Item") -> bool:
    #     """Called when an item is collected in to state. Useful for things such as progressive items or currency."""
    #     name = self.collect_item(state, item)
    #     if name:
    #         state.prog_items[self.player][name] += 1
    #         return True
    #     return False
    #
    # def remove(self, state: "CollectionState", item: "Item") -> bool:
    #     """Called when an item is removed from to state. Useful for things such as progressive items or currency."""
    #     name = self.collect_item(state, item, True)
    #     if name:
    #         state.prog_items[self.player][name] -= 1
    #         if state.prog_items[self.player][name] < 1:
    #             del (state.prog_items[self.player][name])
    #         return True
    #     return False
    #