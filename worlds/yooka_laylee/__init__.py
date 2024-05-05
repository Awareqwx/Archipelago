from .Locations import lookup_name_to_id as locations_lookup_name_to_id
from .Items import (item_table, lookup_name_to_item, lookup_name_to_id as items_lookup_name_to_id)

from .Regions import create_regions, getConnectionName
from .Rules import set_rules
from .Options import yooka_options

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, ItemClassification, Tutorial
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

    data_version = 2
    required_client_version = (1, 0, 0)

    def create_items(self):
        # Set up prefill data for later
        if not hasattr(self.multiworld, "yookaLaylee_prefillItems"):
            self.multiworld.yookaLaylee_prefillItems = {}
        self.multiworld.yookaLaylee_prefillItems[self.player] = {}

        # Decide on which ability to prefill
        firstAbilityOptions = ["Tail Twirl", "Sonar 'Splosion", "Buddy Slam"]
        if self.options.flappy_flight_location == 1:
            firstAbilityOptions = ["Flappy Flight"]
        elif self.options.flappy_flight_location == 2:
            firstAbilityOptions.append("Flappy Flight")
        # We decide on the first ability that we will be using for breaking the chests
        # that contain quillies at the beginning of the game. This ability is guaranteed
        # to show up very early.
        firstAbilityToInsert = self.random.choice(firstAbilityOptions)
        antiBkPagieLocationToUse = None
        antiBkLocationToUse = None
        antiBkItemNameToInsert = None
        # If we're not forcing a local first item, we instead put a damaging ability in the 
        # early_items pool so we don't get completely stuck at the very beginning.
        # If we are forcing a local first item, we don't need to worry about this, since
        # we're guaranteed to not be stuck.
        if not self.options.force_local_first_item:
            self.multiworld.early_items[self.player][firstAbilityToInsert] = 1
        # If we've selected FF for the first ability, we're unblocked from everything.
        # Otherwise, if we want to prevent Tropics BK, we need to insert an ability that
        # can get us to Tropics into a location we can reach.
        if firstAbilityToInsert != "Flappy Flight" and self.options.prevent_tropics_bk:
            antiBkLocations = ["Trowzer's Reptile Roll", "On Top of Capital B Statue"]
            if firstAbilityToInsert == "Buddy Slam": # Can Buddy Slam statue nose for Energy Booster
                antiBkLocations.append("Hivory Towers Energy Booster")
            antiBkItems = ["Reptile Roll"] * 3
            if self.options.flappy_flight_location == 4: # If Anywhere, significantly decrease the odds of rolling FF
                antiBkItems += ["Reptile Roll"] * 6
            if self.options.flappy_flight_location != 3: # As long as FF isn't forced vanilla, it's an option for anti-BK
                antiBkItems.append("Flappy Flight")
            # Set up ability placement info
            antiBkLocationToUse = self.random.choice(antiBkLocations)
            antiBkItemNameToInsert = self.random.choice(antiBkItems)
            # Set up pagie placement info
            antiBkLocations.remove(antiBkLocationToUse)
            antiBkPagieLocationToUse = self.random.choice(antiBkLocations)

        # Generate item pool
        pool = []
        for item in item_table:
            for _ in range(item["quantity"]):
                yooka_item = self.create_item(item["name"])
                if item["name"] == "Flappy Flight" and self.options.flappy_flight_location == 3:
                    self.multiworld.yookaLaylee_prefillItems[self.player]["Trowzer's Flappy Flight"] = yooka_item
                elif item["name"] == firstAbilityToInsert and self.options.force_local_first_item:
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
            "CapitalBPagieCount": self.options.capital_b_pagie_count.value,
            "DisableQuizzes": bool(self.options.disable_quizzes.value),
            "DeathLink": bool(self.options.death_link.value)
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
    game = "Yooka-Laylee"

class YookaItem(Item):
    game = "Yooka-Laylee"
