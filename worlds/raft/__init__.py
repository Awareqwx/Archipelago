import typing
import random

from .Locations import location_table, lookup_name_to_id as locations_lookup_name_to_id
from .Items import item_table, lookup_name_to_item, advancement_item_names
from .Items import lookup_name_to_id as items_lookup_name_to_id
from .Progressives import lookup_item_to_progressive, progressive_item_list

from .Regions import create_regions, getConnectionName
from .Rules import set_rules
from .Options import options

from BaseClasses import Region, RegionType, Entrance, Location, MultiWorld, Item
from ..AutoWorld import World
    
def createResourcePackName(amount: int, itemName: str) -> Item:
    return "Resource Pack: " + str(amount) + " " + itemName

class RaftWorld(World):
    """
    Raft is a flooded world exploration game. You're stranded on a small raft in the middle of the
    ocean, and you must survive on trash floating by you on the top of the water and around/on any
    islands that you come across.
    """
    game: str = "Raft"

    item_name_to_id = items_lookup_name_to_id.copy()
    lastItemId = max(filter(lambda val: val is not None, item_name_to_id.values()))
    for progressiveItemName in progressive_item_list.keys():
        lastItemId += 1
        item_name_to_id[progressiveItemName] = lastItemId
    location_name_to_id = locations_lookup_name_to_id
    options = options

    resourcePackItems = ["Plank", "Plastic", "Clay", "Stone", "Scrap", "SeaVine", "Thatch", "Sand", "Beet", "Rock", "Potato"]
    for packItem in resourcePackItems:
        for i in range(1, 15):
            rpName = createResourcePackName(i, packItem)
            lastItemId += 1
            item_name_to_id[rpName] = lastItemId

    data_version = 12

    def generate_basic(self):
        minRPSpecified = self.world.minimum_resource_pack_amount[self.player].value
        maxRPSpecified = self.world.maximum_resource_pack_amount[self.player].value
        minimumResourcePackAmount = min(minRPSpecified, maxRPSpecified)
        maximumResourcePackAmount = max(minRPSpecified, maxRPSpecified)
        # Generate item pool
        pool = []
        for item in item_table:
            raft_item = self.create_item(item["name"])
            pool.append(raft_item)

        if (self.world.use_resource_packs[self.player].value):
            unusedResourcePackNames = []
            for packItem in self.resourcePackItems:
                for i in range(minimumResourcePackAmount, maximumResourcePackAmount):
                    unusedResourcePackNames.append(createResourcePackName(i, packItem))
            extras = max(min(len(location_table) - len(item_table), len(unusedResourcePackNames)), 0)
            for packItemName in random.sample(unusedResourcePackNames, k=extras):
                pack = self.create_resourcePack(packItemName)
                pool.append(pack)

        self.world.itempool += pool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self):
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        item = lookup_name_to_item[name]
        isFrequency = "Frequency" in name
        shouldUseProgressive = ((isFrequency and self.world.progressive_frequencies[self.player].value)
            or (not isFrequency and self.world.progressive_items[self.player].value))
        if shouldUseProgressive and name in lookup_item_to_progressive:
            name = lookup_item_to_progressive[name]
        return RaftItem(name, item["progression"], self.item_name_to_id[name], player=self.player)
    
    def create_resourcePack(self, rpName: str) -> Item:
        return RaftItem(rpName, False, self.item_name_to_id[rpName], player=self.player)
    
    def collect_item(self, state, item, remove=False):
        if item.name in progressive_item_list:
            prog_table = progressive_item_list[item.name]
            if remove:
                for item_name in reversed(prog_table):
                    if state.has(item_name, item.player):
                        return item_name
            else:
                for item_name in prog_table:
                    if not state.has(item_name, item.player):
                        return item_name

        return super(RaftWorld, self).collect_item(state, item, remove)

    def get_required_client_version(self) -> typing.Tuple[int, int, int]:
        return max((0, 2, 0), super(RaftWorld, self).get_required_client_version())
    
    def pre_fill(self):
        # Victory item
        self.world.get_location("Tangaroa Next Frequency", self.player).place_locked_item(
            RaftItem("Victory", True, None, player=self.player))

def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = locations_lookup_name_to_id.get(location, 0)
            locationObj = RaftLocation(player, location, loc_id, ret)
            ret.locations.append(locationObj)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, getConnectionName(name, exit), ret))

    return ret

class RaftLocation(Location):
    game = "Raft"


class RaftItem(Item):
    game = "Raft"
