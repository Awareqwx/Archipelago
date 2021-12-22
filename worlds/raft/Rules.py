from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin

class RaftLogic(LogicMixin):
    def can_produce_metals(self, player):
        return self.has("Placeable_CookingStand_Smelter", player)
    
    def has_game_basics(self, player):
        return self.has("Bolt", player) and self.has("Hinge", player)

    def can_navigate(self, player): # Sail is added by default and not considered in Archipelago
        return (self.can_produce_metals(player) and self.has_game_basics(player)
            and self.has("Battery", player) and self.has("CircuitBoard", player)
            and self.has("Placeable_Reciever", player) and self.has("Placeable_Reciever_Antenna", player))

    def can_drive(self, player): # The player can go wherever they want with the engine
        return (self.can_produce_metals(player) and self.has_game_basics(player)
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

    # Location rules
    for region in regionMap:
        if region != "Menu":
            # TODO Add item requirements (eg Caravan Island requires zipline for some, but not all, checks)
            for exitRegion in world.get_region(region, player).exits:
                set_rule(world.get_entrance(exitRegion.name, player), regionChecks[region])
     
    # Process locations
    for location in location_table:
        set_rule(world.get_location(location["name"], player), regionChecks[location["region"]])

    # Victory location
    world.completion_condition[player] = lambda state: state.has('Victory', player)
