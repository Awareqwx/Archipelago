from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin
import json
import pkgutil

cashinotokens_table = json.loads(pkgutil.get_data(__name__, "cashinotokens.json").decode())

class YookaLogic(LogicMixin):
    def yooka_can_access_tropics(self, state, player):
        return (self.has("Pagie", player, 1)
                and self.yooka_has_ability(state, player, "<DamagingAbility>")
                and (self.has("Reptile Roll", player) or self.has("Flappy Flight", player)))

    def yooka_can_access_tropics_exp(self, state, player):
        return self.has("Pagie", player, 4) and self.yooka_can_access_tropics(state, player)

    def yooka_can_access_glacier(self, state, player):
        return (self.has("Pagie", player, 7)
                and self.yooka_has_ability(state, player, "<DamagingAbility>")
                and (self.has("Reptile Roll", player) or self.has("Flappy Flight", player)) and self.has("Buddy Slam", player))

    def yooka_can_access_glacier_exp(self, state, player):
        return self.has("Pagie", player, 12) and self.yooka_can_access_glacier(state, player)

    def yooka_can_access_marsh(self, state, player):
        return (self.has("Pagie", player, 19)
                and self.yooka_has_ability(state, player, "<DamagingAbility>")
                and (self.has("Reptile Roll", player) or self.has("Flappy Flight", player)) and self.has("Buddy Slam", player)
                and self.has("Slurp Shot", player) and self.has("Buddy Bubble", player))

    def yooka_can_access_marsh_exp(self, state, player):
        return self.has("Pagie", player, 27) and self.yooka_can_access_marsh(state, player)

    def yooka_can_access_cashino(self, state, player):
        return (self.has("Pagie", player, 37)
                and self.yooka_has_ability(state, player, "<DamagingAbility>")
                and (self.has("Reptile Roll", player) or self.has("Flappy Flight", player)) and self.has("Buddy Slam", player)
                and self.has("Slurp Shot", player) and self.has("Buddy Bubble", player) and self.has("Camo Cloak", player))

    def yooka_can_access_cashino_exp(self, state, player):
        return self.has("Pagie", player, 48) and self.yooka_can_access_cashino(state, player)

    def yooka_can_access_galaxy(self, state, player): #Once abilities are items, this will require Flappy Flight
        return (self.has("Pagie", player, 60)
                and self.yooka_has_ability(state, player, "<DamagingAbility>")
                and self.has("Flappy Flight", player) and self.has("Buddy Slam", player) and self.has("Slurp Shot", player)
                and self.has("Buddy Bubble", player))

    def yooka_can_access_galaxy_exp(self, state, player):
        return self.has("Pagie", player, 75) and self.yooka_can_access_galaxy(state, player)

    def yooka_can_access_end(self, state, player): # Technically don't need Tail Twirl and Sonar Shield, but the final boss is pretty miserable without it
        return (self.has("Pagie", player, 100)
                and self.yooka_has_ability(state, player, "<DamagingAbility>")
                and self.has("Flappy Flight", player) and self.has("Buddy Slam", player) and self.has("Slurp Shot", player)
                and self.has("Buddy Bubble", player) and self.has("Tail Twirl", player) and self.has("Reptile Roll", player)
                and self.has("Sonar Shield", player))

    def yooka_can_get_cashino_token_count(self, state, player, tokenCount):
        accessibleTokenCount = 0
        for tokenGroup in cashinotokens_table:
            if "abilityRequirements" in tokenGroup:
                if self.yooka_has_requirements(state, player, tokenGroup["abilityRequirements"]):
                    accessibleTokenCount += tokenGroup["count"]
            else:
                accessibleTokenCount += tokenGroup["count"]
        return accessibleTokenCount >= tokenCount

    def yooka_has_requirements(self, state, player, requirements, searchMode = 0):
        if isinstance(requirements, str): # Is ability name
            return self.yooka_has_ability(state, player, requirements)
        elif isinstance(requirements, (list, tuple)): # Is list of requirements, searchMode comes into play here
            checkForAnyRequirement = searchMode == 1 # If searchMode is 0 (default), assume AND
            isValid = not checkForAnyRequirement
            for req in requirements:
                isValid = self.yooka_has_requirements(state, player, req)
                if checkForAnyRequirement == isValid:
                    break
            return isValid
        else: # Is object with AND or OR requirement (should never have both)
            if "AND" in requirements:
                if "OR" in requirements:
                    raise Exception(f"Object with both AND and OR present: {str(requirements)}")
                return self.yooka_has_requirements(state, player, requirements["AND"])
            elif "OR" in requirements:
                return self.yooka_has_requirements(state, player, requirements["OR"], 1)
            else:
                raise Exception(f"Invalid requirements: {str(requirements)}")
    
    def yooka_has_ability(self, state, player, ability):
        specialRequirements = {
            "Reptile Rush": lambda state: self.has("Reptile Roll", player) and self.has("Reptile Rush", player),
            "Sonar Shield": lambda state: self.has("Reptile Roll", player) and self.has("Sonar Shield", player),
            "<DamagingAbility>": lambda state: (
                self.has("Tail Twirl", player)
                or self.has("Buddy Slam", player)
                or self.yooka_has_ability(state, player, "Sonar 'Splosion")
                or self.yooka_has_ability(state, player, "Reptile Rush")
                or self.yooka_has_ability(state, player, "Sonar Shield")
            ),
            "<TribalstackPagie>": lambda state: self.yooka_can_access_tropics(state, player), # Wrecked Crow's Nest doesn't spawn until after Tropics entered
            "<ExpandedTribalstackTropics>": lambda state: self.yooka_can_access_tropics_exp(state, player), # Non-expanded pagie but with different options in expansion
            "<GlacierUpperAccess>": lambda state: (
                self.has("Flappy Flight", player)
                or (self.has("Slurp State", player) and (self.has("Tail Twirl", player) or self.has("Glide", player)))
            ),
            "<GlacierLowerAccess>": lambda state: self.has("Buddy Slam", player) and self.has("Sonar Shot", player) and self.yooka_has_ability(state, player, "Reptile Rush"),
            "<GlacierBoss>": lambda state: (
                (self.yooka_has_ability(state, player, "<GlacierUpperAccess>") or self.yooka_has_ability(state, player, "<GlacierLowerAccess>"))
                and self.has("Buddy Slam", player) and self.has("Slurp Shot", player)
            ),
            "<MoodymazeEntry>": lambda state: self.has("Bubble Buddy", player) or self.has("Lizard Lash", player) or self.has("Flappy Flight", player),
            "<CashinoEntry>": lambda state: self.has("Camo Cloak", player) or self.has("Flappy Flight", player),
            "<ExpandedCashino>": lambda state: self.yooka_can_access_cashino_exp(state, player), # Specifically for Cashino tokens requirements
            "<GalaxyEntry>": lambda state: self.has("Flappy Flight", player) or self.has("Glide", player) or self.has("Health Booster", player, 5)
        }
        if ability in specialRequirements:
            return specialRequirements[ability](state)
        elif "<CashinoTokens" in ability:
            tokenLevel = int(ability.removeprefix("<CashinoTokens").removesuffix(">"))
            return self.yooka_can_get_cashino_token_count(state, player, tokenLevel * 10)
        elif "<(" in ability:
            itemRequired = ability.removeprefix("<(").rsplit(")", 1)[0].strip()
            numberRequired = ability.removeprefix("<(").rsplit(")", 1)[1].strip().removeprefix("x").removesuffix(">")
            return self.has(itemRequired, player, int(numberRequired))
        elif "<" in ability:
            raise Exception("Unknown special requirement: " + ability)
        else:
            return self.has(ability, player)

def set_rules(world, player):
    regionChecks = {
        "Shipwreck Creek": lambda state: True,
        "Hivory Towers Entrance": lambda state: state.yooka_has_ability(state, player, "<DamagingAbility>"),
        "Hivory Towers Hub B": lambda state: state.yooka_has_ability(state, player, "<DamagingAbility>"),
        "Hivory Towers Archive": lambda state: state.yooka_has_ability(state, player, "<DamagingAbility>"),
        "Hivory Towers Waterworks": lambda state: state.yooka_has_ability(state, player, "<DamagingAbility>"),
        "Hivory Towers Outside (NoFlight)": lambda state: state.yooka_has_ability(state, player, "<DamagingAbility>"),
        "Hivory Towers Outside (Flight)": lambda state: state.yooka_has_ability(state, player, "<DamagingAbility>"),
        "Tribalstack Tropics": lambda state: state.yooka_can_access_tropics(state, player),
        "Expanded Tropics": lambda state: state.yooka_can_access_tropics_exp(state, player),
        "Glitterglaze Glacier": lambda state: state.yooka_can_access_glacier(state, player),
        "Expanded Glacier": lambda state: state.yooka_can_access_glacier_exp(state, player),
        "Moodymaze Marsh": lambda state: state.yooka_can_access_marsh(state, player),
        "Expanded Marsh": lambda state: state.yooka_can_access_marsh_exp(state, player),
        "Capital Cashino": lambda state: state.yooka_can_access_cashino(state, player),
        "Expanded Cashino": lambda state: state.yooka_can_access_cashino_exp(state, player),
        "Galleon Galaxy": lambda state: state.yooka_can_access_galaxy(state, player),
        "Expanded Galaxy": lambda state: state.yooka_can_access_galaxy_exp(state, player),
        "Endgame": lambda state: state.yooka_can_access_end(state, player)
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
            if canAccess and "requiresAbilities" in location:
                canAccess = state.yooka_has_requirements(state, player, location["requiresAbilities"])
            return canAccess
        set_rule(locFromWorld, fullLocationCheck)

    # Victory requirement
    world.completion_condition[player] = lambda state: state.has("Victory", player)