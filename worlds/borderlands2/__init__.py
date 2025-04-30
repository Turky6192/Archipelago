from __future__ import annotations

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

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


    # def generate_early(self) -> None:
    #     """
    #     Run before any general steps of the MultiWorld other than options. Useful for getting and adjusting option
    #     results and determining layouts for entrance rando etc. start inventory gets pushed after this step.
    #     """
    #     pass
    #
    # def create_regions(self) -> None:
    #     """Method for creating and connecting regions for the World."""
    #     pass
    #
    # def create_items(self) -> None:
    #     """
    #     Method for creating and submitting items to the itempool. Items and Regions must *not* be created and submitted
    #     to the MultiWorld after this step. If items need to be placed during pre_fill use `get_prefill_items`.
    #     """
    #     pass
    #
    # def set_rules(self) -> None:
    #     """Method for setting the rules on the World's regions and locations."""
    #     pass
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
    # def create_item(self, name: str) -> "Item":
    #     """
    #     Create an item for this world type and player.
    #     Warning: this may be called with self.world = None, for example by MultiServer
    #     """
    #     raise NotImplementedError
    #
    # def get_filler_item_name(self) -> str:
    #     """Called when the item pool needs to be filled with additional items to match location count."""
    #     logging.warning(f"World {self} is generating a filler item without custom filler pool.")
    #     return self.multiworld.random.choice(tuple(self.item_name_to_id.keys()))
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
    # # following methods should not need to be overridden.
    # def create_filler(self) -> "Item":
    #     return self.create_item(self.get_filler_item_name())
    #
    # # convenience methods
    # def get_location(self, location_name: str) -> "Location":
    #     return self.multiworld.get_location(location_name, self.player)
    #
    # def get_locations(self) -> "Iterable[Location]":
    #     return self.multiworld.get_locations(self.player)
    #
    # def get_entrance(self, entrance_name: str) -> "Entrance":
    #     return self.multiworld.get_entrance(entrance_name, self.player)
    #
    # def get_entrances(self) -> "Iterable[Entrance]":
    #     return self.multiworld.get_entrances(self.player)
    #
    # def get_region(self, region_name: str) -> "Region":
    #     return self.multiworld.get_region(region_name, self.player)
    #
    # def get_regions(self) -> "Iterable[Region]":
    #     return self.multiworld.get_regions(self.player)
    #
    # def push_precollected(self, item: Item) -> None:
    #     self.multiworld.push_precollected(item)
    #
    # @property
    # def player_name(self) -> str:
    #     return self.multiworld.get_player_name(self.player)
    #
    # @classmethod
    # def get_data_package_data(cls) -> "GamesPackage":
    #     sorted_item_name_groups = {
    #         name: sorted(cls.item_name_groups[name]) for name in sorted(cls.item_name_groups)
    #     }
    #     sorted_location_name_groups = {
    #         name: sorted(cls.location_name_groups[name]) for name in sorted(cls.location_name_groups)
    #     }
    #     res: "GamesPackage" = {
    #         # sorted alphabetically
    #         "item_name_groups": sorted_item_name_groups,
    #         "item_name_to_id": cls.item_name_to_id,
    #         "location_name_groups": sorted_location_name_groups,
    #         "location_name_to_id": cls.location_name_to_id,
    #     }
    #     res["checksum"] = data_package_checksum(res)
    #     return res
