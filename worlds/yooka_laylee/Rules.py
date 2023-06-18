from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin

class YookaLogic(LogicMixin):
    
    def yooka_can_access_tropics(self, player): #Once abilities are items, this will require Reptile Roll
        return self.has("Pagie", player, 1)

    def yooka_can_access_tropics_exp(self, player):
        return self.has("Pagie", player, 4)

    def yooka_can_access_glacier(self, player): #Once abilities are items, this will require Glide
        return self.has("Pagie", player, 7)

    def yooka_can_access_glacier_exp(self, player):
        return self.has("Pagie", player, 12)

    def yooka_can_access_marsh(self, player): #Once abilities are items, this will require Buddy Bubble
        return self.has("Pagie", player, 19)

    def yooka_can_access_marsh_exp(self, player):
        return self.has("Pagie", player, 27)

    def yooka_can_access_cashino(self, player): #Once abilities are items, this will require Camo Cloak
        return self.has("Pagie", player, 37)

    def yooka_can_access_cashino_exp(self, player):
        return self.has("Pagie", player, 48)

    def yooka_can_access_galaxy(self, player): #Once abilities are items, this will require Flappy Flight
        return self.has("Pagie", player, 60)

    def yooka_can_access_galaxy_exp(self, player):
        return self.has("Pagie", player, 75)

    def yooka_can_access_end(self, player):
        return self.has("Pagie", player, 100)



def set_rules(world, player):
    regionChecks = {
        "Hivory Towers": lambda state: True,
        "Tribalstack Tropics": lambda state: state.yooka_can_access_tropics(player),
        "Expanded Tropics": lambda state: state.yooka_can_access_tropics_exp(player),
        "Glitterglaze Glacier": lambda state: state.yooka_can_access_glacier(player),
        "Expanded Glacier": lambda state: state.yooka_can_access_glacier_exp(player),
        "Moodymaze Marsh": lambda state: state.yooka_can_access_marsh(player),
        "Expanded Marsh": lambda state: state.yooka_can_access_marsh_exp(player),
        "Capital Cashino": lambda state: state.yooka_can_access_cashino(player),
        "Expanded Cashino": lambda state: state.yooka_can_access_cashino_exp(player),
        "Galleon Galaxy": lambda state: state.yooka_can_access_galaxy(player),
        "Expanded Galaxy": lambda state: state.yooka_can_access_galaxy_exp(player),
        "Endgame": lambda state: state.yooka_can_access_end(player)
    }
    itemChecks = {
        "Pagie": lambda state: True,
    }
    abilityChecks = {
        "Buddy Bubble": lambda state: state.yooka_can_access_marsh(player), #Once abilities are items, this will change
        "Buddy Slam": lambda state: state.yooka_can_access_tropics(player),
        "Camo Cloak": lambda state: state.yooka_can_access_cashino(player),
        "Flappy Flight": lambda state: state.yooka_can_access_galaxy(player),
        "Glide": lambda state: state.yooka_can_access_glacier(player),
        "Lizard Lash": lambda state: state.yooka_can_access_marsh(player),
        "Lizard Leap": lambda state: state.yooka_can_access_glacier(player),
        "Reptile Roll": lambda state: state.yooka_can_access_tropics(player),
        "Reptile Rush": lambda state: state.yooka_can_access_cashino(player),
        "Slurp Shot": lambda state: state.yooka_can_access_tropics(player),
        "Slurp State": lambda state: state.yooka_can_access_glacier(player),
        "Sonar 'Splosion": lambda state: state.yooka_can_access_marsh(player),
        "Sonar Shield": lambda state: state.yooka_can_access_galaxy(player),
        "Sonar Shot": lambda state: state.yooka_can_access_tropics(player),
        "Update Me": lambda state: True #Placeholder - Fill in actual ability requirements
    }

    # Region access rules
    for region in regionMap:
        if region != "Menu":
            for exitRegion in world.get_region(region, player).exits:
                set_rule(world.get_entrance(exitRegion.name, player), regionChecks[region])

    # Location access rules
    for location in location_table:
        locFromWorld = world.get_location(location["name"], player)
        def fullLocationCheck(state, location=location):
            canAccess = regionChecks[location["region"]](state)
            if "requiresAbilities" in location:
                for ability in location["requiresAbilities"]:
                    if not abilityChecks[ability](state):
                        canAccess = False
                        break
            if "requiresItems" in location:
                for item in location["requiresItems"]:
                    if not state.has(player, item):
                        canAccess = False
                        break
            return canAccess
        set_rule(locFromWorld, fullLocationCheck)

    # Victory requirement
    world.completion_condition[player] = lambda state: state.has("Victory", player)