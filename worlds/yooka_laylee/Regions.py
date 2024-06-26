import json
import pkgutil
from BaseClasses import Entrance

regionMap = json.loads(pkgutil.get_data(__name__, "regions.json").decode())

def create_regions(world, player: int):
    from . import create_region
    from .Locations import location_table
    
    # Create regions and assign locations to each region
    for region in regionMap:
        exit_array = regionMap[region]
        if len(exit_array) == 0:
            exit_array = None
        new_region = create_region(world, player, region, [location["name"] for location in location_table if location["region"] == region], exit_array)
        world.regions += [new_region]

    menu = create_region(world, player, "Menu", None, ["Shipwreck Creek"])
    world.regions += [menu]
    menuConn = world.get_entrance("MenuToShipwreck Creek", player)
    menuConn.connect(world.get_region("Shipwreck Creek", player))

    # Link regions together
    for region in regionMap:
        for linkedRegion in regionMap[region]:
            connection = world.get_entrance(getConnectionName(region, linkedRegion), player)
            connection.connect(world.get_region(linkedRegion, player))

def getConnectionName(entranceName: str, exitName: str):
    return entranceName + "To" + exitName