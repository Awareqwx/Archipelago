import typing
import random
import logging

from .Locations import location_table, lookup_name_to_id as locations_lookup_name_to_id, priority_locations as locations_priority_locations
from .Items import (item_table, lookup_name_to_item, lookup_name_to_id as items_lookup_name_to_id)

from .Regions import create_regions, getConnectionName
from .Rules import set_rules
from .Options import yooka_options

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, ItemClassification, Tutorial, LocationProgressType
from ..AutoWorld import World, WebWorld


class YookaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Yooka-Laylee integration for Archipelago multiworld games.",
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
    game: str = "Yooka-Laylee"
    web = YookaWeb()

    item_name_to_id = items_lookup_name_to_id.copy()
    lastItemId = max(filter(lambda val: val is not None, item_name_to_id.values()))

    location_name_to_id = locations_lookup_name_to_id
    option_definitions = yooka_options

    data_version = 1
    required_client_version = (0, 4, 2)

    def create_items(self):
        # TODO Add an option for how likely Flappy Flight shows up early. Range 0-100, 0 being never and 100 being always. Or something like that.
        if not self.multiworld.prevent_tropics_bk[self.player]:
            logging.warn("Yooka-Laylee: Prevent Tropics BK not enabled. World generation may fail with only Yooka-Laylee worlds.")

        # Set up prefill data for later
        if not hasattr(self.multiworld, "yookaLaylee_prefillItems"):
            self.multiworld.yookaLaylee_prefillItems = {}
        self.multiworld.yookaLaylee_prefillItems[self.player] = {}

        # Decide on which ability to prefill
        firstAbilityOptions = ["Tail Twirl", "Sonar 'Splosion", "Buddy Slam", "Flappy Flight"]
        if self.multiworld.flappy_flight_location[self.player] == 1:
            firstAbilityOptions = ["Flappy Flight"]
        elif self.multiworld.flappy_flight_location[self.player] == 2:
            firstAbilityOptions.append("Flappy Flight")
        damagingAbilityToInsert = self.multiworld.random.choice(firstAbilityOptions)
        antiBkPagieLocationToUse = None
        antiBkLocationToUse = None
        antiBkItemNameToInsert = None
        if not self.multiworld.force_local_first_item[self.player]:
            self.multiworld.early_items[self.player][damagingAbilityToInsert] = 1
        if damagingAbilityToInsert != "Flappy Flight" and self.multiworld.prevent_tropics_bk[self.player]:
            antiBkLocations = ["Trowzer's Reptile Roll", "On Top of Capital B Statue"]
            if damagingAbilityToInsert == "Buddy Slam":
                antiBkLocations.append("Hivory Towers Energy Booster")
            antiBkItems = ["Reptile Roll", "Reptile Roll", "Reptile Roll"]
            if self.multiworld.flappy_flight_location[self.player] != 3:
                antiBkItems.append("Flappy Flight") # 25% chance for FF if allowed
            # Set up ability placement info
            antiBkLocationToUse = self.multiworld.random.choice(antiBkLocations)
            antiBkItemNameToInsert = self.multiworld.random.choice(antiBkItems)
            # Set up pagie placement info
            antiBkLocations.remove(antiBkLocationToUse)
            antiBkPagieLocationToUse = self.multiworld.random.choice(antiBkLocations)

        # Generate item pool
        pool = []
        for item in item_table:
            for _ in range(item["quantity"]):
                yooka_item = self.create_item(item["name"])
                if item["name"] == "Flappy Flight" and self.multiworld.flappy_flight_location[self.player] == 3:
                    self.multiworld.yookaLaylee_prefillItems[self.player]["Trowzer's Flappy Flight"] = yooka_item
                elif item["name"] == damagingAbilityToInsert and self.multiworld.force_local_first_item[self.player]:
                    self.multiworld.yookaLaylee_prefillItems[self.player]["Trowzer's Tail Twirl"] = yooka_item
                elif item["name"] == antiBkItemNameToInsert:
                    self.multiworld.yookaLaylee_prefillItems[self.player][antiBkLocationToUse] = yooka_item
                elif item["name"] == "Pagie" and antiBkPagieLocationToUse != None:
                    self.multiworld.yookaLaylee_prefillItems[self.player][antiBkPagieLocationToUse] = yooka_item
                    antiBkPagieLocationToUse = None
                else:
                    pool.append(yooka_item)
        self.multiworld.itempool += pool

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player)
    
    def get_pre_fill_items(self):
        return [loc.item for loc in self.multiworld.get_filled_locations(self.player)]

    def create_item(self, name: str) -> Item:
        item = lookup_name_to_item[name]
        itemClassification = ItemClassification.useful
        if item["name"] == "Pagie":
            itemClassification = ItemClassification.progression_skip_balancing
        elif item["progression"]:
            itemClassification = ItemClassification.progression
        return YookaItem(name, itemClassification, self.item_name_to_id[name], player=self.player)
    
    def create_resourcePack(self, rpName: str) -> Item:
        return YookaItem(rpName, ItemClassification.filler, self.item_name_to_id[rpName], player=self.player)

    def pre_fill(self):
        # Prefill all predetermined items in their relevant locations
        for locationName, itemToInsert in self.multiworld.yookaLaylee_prefillItems[self.player].items():
            self.multiworld.get_location(locationName, self.player).place_locked_item(itemToInsert)
        self.multiworld.yookaLaylee_prefillItems.pop(self.player) # Clean up references

        # Victory item
        self.multiworld.get_location("Game Complete", self.player).place_locked_item(
            YookaItem("Victory", ItemClassification.progression, None, player=self.player))

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
            if location in locations_priority_locations:
                locationObj.progress_type = LocationProgressType.PRIORITY
            ret.locations.append(locationObj)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, getConnectionName(name, exit), ret))
    return ret

class YookaLocation(Location):
    game = "Yooka-Laylee"

class YookaItem(Item):
    game = "Yooka-Laylee"