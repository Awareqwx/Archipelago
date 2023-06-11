import typing
import random

from .Locations import location_table, lookup_name_to_id as locations_lookup_name_to_id
from .Items import (item_table, lookup_name_to_item, lookup_name_to_id as items_lookup_name_to_id)

from .Regions import create_regions, getConnectionName
from .Rules import set_rules
from .Options import yooka_options

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, ItemClassification, Tutorial
from ..AutoWorld import World, WebWorld


class YookaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Yooka Laylee integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SunnyBat", "Awareqwx"]
    )]


class YookaWorld(World):
    """
    Yooka-Laylee is a charming 3D platformer where players control Yooka, a chameleon, and Laylee, a bat,
    as they jump, glide, and roll through vibrant levels filled with puzzles, enemies, and collectibles.
    With a variety of abilities and quirky characters to encounter, players must utilize their skills to
    defeat enemies, uncover secrets, and save the day from the nefarious Capital B.
    """
    game: str = "Yooka Laylee"
    web = YookaWeb()

    item_name_to_id = items_lookup_name_to_id.copy()
    lastItemId = max(filter(lambda val: val is not None, item_name_to_id.values()))

    location_name_to_id = locations_lookup_name_to_id
    option_definitions = yooka_options

    data_version = 1
    required_client_version = (0, 3, 4)

    def create_items(self):
        # Generate item pool
        pool = []
        for item in item_table:
            
            for i in range(0, item["quantity"]):
                yooka_item = self.create_item(item["name"])
                pool.append(yooka_item)

        self.multiworld.itempool += pool

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player)
    
    def get_pre_fill_items(self):
        return []

    def create_item(self, name: str) -> Item:
        item = lookup_name_to_item[name]
        return YookaItem(name, ItemClassification.progression if item["progression"] else ItemClassification.filler,
                        self.item_name_to_id[name], player=self.player)
    
    def create_resourcePack(self, rpName: str) -> Item:
        return YookaItem(rpName, ItemClassification.filler, self.item_name_to_id[rpName], player=self.player)
    
    #TODO: Delete if unnecessary
    # def collect_item(self, state, item, remove=False):
    #     if item.name in progressive_item_list:
    #         prog_table = progressive_item_list[item.name]
    #         if remove:
    #             for item_name in reversed(prog_table):
    #                 if state.has(item_name, item.player):
    #                     return item_name
    #         else:
    #             for item_name in prog_table:
    #                 if not state.has(item_name, item.player):
    #                     return item_name

    #     return super(YookaWorld, self).collect_item(state, item, remove)

    def pre_fill(self):
        # Victory item
        self.multiworld.get_location("Game Complete", self.player).place_locked_item(
            YookaItem("Victory", ItemClassification.progression, None, player=self.player))
    
    def setLocationItem(self, location: str, itemName: str):
        itemToUse = next(filter(lambda itm: itm.name == itemName, self.multiworld.itempool))
        self.multiworld.itempool.remove(itemToUse)
        self.multiworld.get_location(location, self.player).place_locked_item(itemToUse)
    
    def setLocationItemFromRegion(self, region: str, itemName: str):
        itemToUse = next(filter(lambda itm: itm.name == itemName, self.multiworld.itempool))
        self.multiworld.itempool.remove(itemToUse)
        location = random.choice(list(loc for loc in location_table if loc["region"] == region))
        self.multiworld.get_location(location["name"], self.player).place_locked_item(itemToUse)

    def fill_slot_data(self):
        return {
            "DeathLink": bool(self.multiworld.death_link[self.player].value)
        }

def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, player, world)
    if locations:
        for location in locations:
            loc_id = locations_lookup_name_to_id.get(location, 0)
            locationObj = YookaLocation(player, location, loc_id, ret)
            ret.locations.append(locationObj)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, getConnectionName(name, exit), ret))
    return ret

class YookaLocation(Location):
    game = "Yooka Laylee"


class YookaItem(Item):
    game = "Yooka Laylee"
