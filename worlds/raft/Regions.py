import json
import os
from BaseClasses import Entrance

with open(os.path.join(os.path.dirname(__file__), 'regions.json'), 'r') as file:
    regionMap = json.loads(file.read())

def create_regions(world, player: int):
    from . import create_region
    from .Locations import location_table
    
    # Create regions and assign locations to each region
    for region in regionMap:
        exit_array = regionMap[region]
        if len(exit_array) == 0:
            exit_array = None
        new_region = create_region(world, player, region, [location["location"] for location in location_table if location["region"] == region], exit_array)
            
        world.regions += [new_region]