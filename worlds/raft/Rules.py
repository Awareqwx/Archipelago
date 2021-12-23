from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin

class RaftLogic(LogicMixin):
    def can_smelt_items(self, player):
        return self.has("Placeable_CookingStand_Smelter", player)

    def can_craft_bolt(self, player):
        return self.can_smelt_items(player) and self.has("Bolt", player)

    def can_craft_hinge(self, player):
        return self.can_smelt_items(player) and self.has("Hinge", player)

    def can_craft_circuitBoard(self, player):
        return self.can_smelt_items(player) and self.has("CircuitBoard", player)

    def can_craft_plasticBottle(self, player):
        return self.can_smelt_items(player) and self.has("PlasticBottle_Empty", player)

    def can_craft_shears(self, player):
        return self.can_smelt_items(player) and self.can_craft_hinge(player) and self.has("Shear", player)

    def can_get_dirt(self, player):
        return self.has("Shovel", player)

    def can_capture_animals(self, player):
        return (self.can_smelt_items(player) and self.can_craft_bolt(player) # Required for crafting
            and self.has("NetCanister", player) and self.has("NetGun", player)
            and self.has("Placeable_Cropplot_Grass", player) and self.can_get_dirt(player))
    
    def has_game_basics(self, player):
        return self.can_craft_bolt(player) and self.can_craft_hinge(player)

    def can_navigate(self, player): # Sail is added by default and not considered in Archipelago
        return (self.can_smelt_items(player) and self.has_game_basics(player)
            and self.has("Battery", player) and self.has("CircuitBoard", player)
            and self.has("Placeable_Reciever", player) and self.has("Placeable_Reciever_Antenna", player))

    def can_drive(self, player): # The player can go wherever they want with the engine
        return (self.can_smelt_items(player) and self.has_game_basics(player)
            and self.has("Placeable_MotorWheel", player) and self.has("Placeable_SteeringWheel", player))

    def can_access_radio_tower(self, player):
        # Technically the player doesn't need things like the sail to reach the Radio Tower,
        # but paddling there is not very efficient or engaging gameplay.
        return self.can_navigate(player)

    def can_complete_radio_tower(self, player):
        return self.can_access_radio_tower(player)

    def can_access_vasagatan(self, player):
        return self.can_complete_radio_tower(player) and self.can_navigate(player) and self.has("NoteBookNote_Index2_Post-it", player)

    def can_complete_vasagatan(self, player):
        return self.can_access_vasagatan(player)

    def can_access_balboa_island(self, player):
        return self.can_complete_vasagatan(player) and self.can_drive(player) and self.has("NoteBookNote_Index17_Vasagatan_PostItNote_FrequencyToBalboa", player)

    def can_complete_balboa_island(self, player):
        return self.can_access_balboa_island(player) and self.has("Machete", player)

    def can_access_caravan_island(self, player):
        return self.can_complete_balboa_island(player) and self.can_drive(player) # Coordinates are given from Relay Station quest

    def can_complete_caravan_island(self, player):
        return self.can_access_caravan_island(player) and self.has("ZiplineTool", player)

    def can_access_tangaroa(self, player):
        return self.can_complete_caravan_island(player) and self.can_drive(player) and self.has("NoteBookNote_Index43_Landmark_CaravanIsland_FrequencyToTangaroa", player)

    def can_complete_tangaroa(self, player):
        return self.can_access_tangaroa(player)

def set_rules(world, player):
    # Map region to check to see if we can access it
    regionChecks = {
        "Raft": lambda state: True,
        "ResearchTable": lambda state: True,
        "RadioTower": lambda state: state.can_access_radio_tower(player), # All can_access functions have state as implicit parameter for function
        "RadioTowerCompletion": lambda state: state.can_complete_radio_tower(player),
        "Vasagatan": lambda state: state.can_access_vasagatan(player),
        "VasagatanCompletion": lambda state: state.can_complete_vasagatan(player),
        "BalboaIsland": lambda state: state.can_access_balboa_island(player),
        "BalboaIslandCompletion": lambda state: state.can_complete_balboa_island(player),
        "CaravanIsland": lambda state: state.can_access_caravan_island(player),
        "CaravanIslandCompletion": lambda state: state.can_complete_caravan_island(player),
        "Tangaroa": lambda state: state.can_access_tangaroa(player),
        "TangaroaCompletion": lambda state: state.can_complete_tangaroa(player)
    }
    itemChecks = {
        "Plank": lambda state: True,
        "Plastic": lambda state: True,
        "Clay": lambda state: True,
        "Stone": lambda state: True,
        "Rope": lambda state: True,
        "Nail": lambda state: True,
        "Scrap": lambda state: True,
        "Leather": lambda state: True, # Wiki has conflicting information on whether Large Islands before Radio Tower has been visited; pretty sure they can
        "SeaVine": lambda state: True,
        "Brick_Dry": lambda state: True,
        "Feather": lambda state: True,
        "Thatch": lambda state: True, # Palm Leaf
        "Placeable_GiantClam": lambda state: True,
        "MetalIngot": lambda state: state.can_smelt_items(player),
        "CopperIngot": lambda state: state.can_smelt_items(player),
        "VineGoo": lambda state: state.can_smelt_items(player),
        "ExplosivePowder": lambda state: state.can_smelt_items(player),
        "Glass": lambda state: state.can_smelt_items(player),
        "Bolt": lambda state: state.can_craft_bolt(player),
        "Hinge": lambda state: state.can_craft_hinge(player),
        "CircuitBoard": lambda state: state.can_craft_circuitBoard(player),
        "PlasticBottle_Empty": lambda state: state.can_craft_plasticBottle(player),
        "Shear": lambda state: state.can_craft_shears(player),
        "Wool": lambda state: state.can_capture_animals(player) and state.can_craft_shears(player),
        "HoneyComb": lambda state: state.can_access_balboa_island(player),
        "Jar_Bee": lambda state: state.can_access_balboa_island(player) and state.can_smelt_items(player),
        "Dirt": lambda state: state.can_get_dirt(player),
        "Egg": lambda state: state.can_capture_animals(player)
    }

    # Location rules
    for region in regionMap:
        if region != "Menu":
            # TODO Add item requirements (eg Caravan Island requires zipline for some, but not all, checks)
            for exitRegion in world.get_region(region, player).exits:
                set_rule(world.get_entrance(exitRegion.name, player), regionChecks[region])
     
    # Process locations
    for location in location_table:
        locFromWorld = world.get_location(location["name"], player)
        if "requiresAccessToItems" in location:
            def ruleLambda(state):
                canAccess = regionChecks[location["region"]](state)
                for item in locFromWorld["requiresAccessToItems"]:
                    if not itemChecks[item](state):
                        canAccess = False
                        break
                return canAccess
            set_rule(locFromWorld, ruleLambda)
        else:
            set_rule(locFromWorld, regionChecks[location["region"]])

    # Victory location
    world.completion_condition[player] = lambda state: state.has('Victory', player)

    # Crafting Table requirements
