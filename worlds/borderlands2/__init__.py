from __future__ import annotations

import logging
from typing import List, Dict

from Options import OptionError
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, LocationProgressType
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule

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
    explicit_indirect_conditions: False

    selected_dlc: List[str] = []
    origin_region_name = "Meet Claptrap"
    pooled_skills: int
    excluded_opt_missions: List[str] = []

    player_location_pool: Dict[str, int]

    def generate_early(self) -> None:
        # Verify a specific character is chosen if skill rando is set to "skills in pool"
        self.pooled_skills = self.options.extra_skills
        if self.options.skill_randomization > 0:
            self.pooled_skills += self.options.max_level - 3
        if self.options.character == 0 and self.options.skill_randomization == 2:
            logging.warning("Borderlands 2: Player %s (%s has Skill Randomization set to "
                              "'Skills in Pool' but did not select a specific character. Using 'Points in Pool instead.",
                            self.player, self.player_name)

        # Verify that the player can reach all level locations wanted with chosen DLC options
        selected_dlc = list(self.options.allowed_dlc)
        if self.options.max_level > 50:
            level_dlc =  {"UVHM 1": 11, "UVHM 2": 11, "Fight for Sanctuary": 8}
            allowed_max = 50 + sum(level_dlc[dlc] for dlc in level_dlc if dlc in selected_dlc)
            if allowed_max < self.options.max_level:
                raise OptionError(f"Borderlands 2: Player {self.player} ({self.player_name} does not have required DLCs"
                                  f" enabled to reach desired Max Level ({self.options.max_level}).)")

    def create_regions(self) -> None:
        self.player_location_pool = self.location_name_to_id.copy()

        # Removes levels from location pool above selected max level
        if self.options.max_level < 80:
            for level in range(self.options.max_level + 1, 81):
                del self.player_location_pool[f"Level {level}"]

        working_opt_mission = optional_mission_list.copy()
        self.random.shuffle(working_opt_mission)
        for _ in range(len(working_opt_mission) // 4):
            excluded = working_opt_mission.pop()
            self.excluded_opt_missions.append(excluded)

        for region_name in story_region_names:
            region = Region(region_name, self.player, self.multiworld)
            mapped_loc_per_region = {name: id for name, id in self.player_location_pool.items() if name in region_location_map[region_name]}
            region.add_locations(mapped_loc_per_region)
            self.multiworld.regions.append(region)

        jack_region = self.get_region("Meet The Warrior")
        jack_region.locations.append(Borderlands2Location(self.player, "Kill Jack", None, jack_region))

        for exit_index, region_name in enumerate(story_region_names[:-1]):
            region = self.get_region(region_name)
            exit_region = self.get_region(story_region_names[exit_index + 1])
            region.connect(exit_region, f"Story Progress {exit_index + 1}")

        self.multiworld.get_location("Kill Jack", self.player).place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        set_rule(self.multiworld.get_location("Kill Jack", self.player), lambda state: state.has("Progressive Story Mission", self.player, 18))

        #from Utils import visualize_regions
        #visualize_regions(self.multiworld.get_region("Meet Claptrap", self.player), "my_world.puml")

    def create_item(self, name: str) -> Borderlands2Item:
        item_data = item_data_table[name]
        item_class = item_data.i_class
        return Borderlands2Item(name, item_class, self.item_name_to_id[name], self.player)

    def create_event(self, event: str) -> Borderlands2Item:
        return Borderlands2Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        borderlands2_items: List[Borderlands2Item] = []
        # Story missions are the main bottleneck so they always need added
        borderlands2_items += [self.create_item("Progressive Story Mission") for _ in range(18)]

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
        if self.options.character == 0 or self.options.character > 0 and self.options.skill_randomization < 2:
            borderlands2_items += [self.create_item("Skill Point") for _ in range(self.pooled_skills)]
        elif self.options.character > 0 and self.options.skill_randomization == 2:
            skills = get_skills(self.options.character, self.pooled_skills + 5)
            for skill in skills:
                skill_item = self.create_item(skill)
                borderlands2_items.append(skill_item)

        for item in optional_mission_items:
            if item.removesuffix(" Unlock") in self.excluded_opt_missions:
                excluded_item = Borderlands2Item(item, ItemClassification.progression_skip_balancing, self.item_name_to_id[item], self.player)
                borderlands2_items.append(excluded_item)
            else:
                opt_mission_item = self.create_item(item)
                borderlands2_items.append(opt_mission_item)

        self.multiworld.itempool += borderlands2_items
        remaining_locs = len(self.multiworld.get_unfilled_locations(self.player)) - len(borderlands2_items)
        for _ in range(remaining_locs):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))



    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def set_rules(self) -> None:
    #     """Method for setting the rules on the World's regions and locations."""
        for location in self.get_locations():
            if location.name in self.excluded_opt_missions:
                location.progress_type = LocationProgressType.EXCLUDED
            if location.name in optional_mission_list:
                set_rule(self.multiworld.get_location(location.name, self. player),
                         lambda state, name=location.name: state.has(f"{name} Unlock", self.player))
        region_count = 0
        region_index_list: Dict[str, int] = {}
        for region in story_region_names:
            region_index_list[region] = region_count
            region_count += 1

        for region_name in story_region_names:
            for location in self.get_region(region_name).locations:
                set_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state, value=min(region_index_list[region_name], 18):
                         state.has("Progressive Story Mission", self.player, value))
            if 19 > region_index_list[region_name] > 4 and self.options.skill_randomization > 0:
                set_rule(self.get_entrance(f"Story Progress {region_index_list[region_name] + 1}"),
                         lambda state, value=min(region_index_list[region_name], 18): state.has(
                             "Progressive Story Mission", self.player, value) and
                         state.has_from_list(skill_items, self.player, int(value * 1.8 - 5)))
            elif region_index_list[region_name] < 19:
                set_rule(self.get_entrance(f"Story Progress {region_index_list[region_name] + 1}"),
                         lambda state, value=min(region_index_list[region_name], 18):
                         state.has("Progressive Story Mission", self.player, value))


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
    # def pre_fill(self) -> None:
    #     """Optional method that is supposed to be used for special fill stages. This is run *after* plando."""
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
    # def fill_slot_data(self) -> Mapping[str, Any]:  # json of WebHostLib.models.Slot
    #     """
    #     What is returned from this function will be in the `slot_data` field
    #     in the `Connected` network package.
    #     It should be a `dict` with `str` keys, and should be serializable with json.
    #
    #     This is a way the generator can give custom data to the client.
    #     The client will receive this as JSON in the `Connected` response.
    #
    #     The generation does not wait for `generate_output` to complete before calling this.
    #     `threading.Event` can be used if you need to wait for something from `generate_output`.
    #     """
    #     # The reason for the `Mapping` type annotation, rather than `dict`
    #     # is so that type checkers won't worry about the mutability of `dict`,
    #     # so you can have more specific typing in your world implementation.
    #     return {}
    #
    # def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
    #     """
    #     Fill in additional entrance information text into locations, which is displayed when hinted.
    #     structure is {player_id: {location_id: text}} You will need to insert your own player_id.
    #     """
    #     pass
    #
    # def modify_multidata(self, multidata: Dict[str, Any]) -> None:  # TODO: TypedDict for multidata?
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
    #     # TODO remove loop when worlds use options dataclass
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