from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin
import json
import pkgutil

cashinotokens_table = json.loads(pkgutil.get_data(__name__, "cashinotokens.json").decode())

class YookaLayleeLogic(LogicMixin):
    yookaLaylee_specialRequirements = {
        "Reptile Rush": lambda state, player: state.has("Reptile Roll", player) and state.has("Reptile Rush", player),
        "Sonar Shield": lambda state, player: state.has("Reptile Roll", player) and state.has("Sonar Shield", player),
        "<DamagingAbility>": lambda state, player: (
            state.has("Tail Twirl", player)
            or state.has("Buddy Slam", player)
            or state.yookaLaylee_has_requirements("Sonar 'Splosion", player)
            or state.yookaLaylee_has_requirements("Reptile Rush", player)
            or state.yookaLaylee_has_requirements("Sonar Shield", player)
        ),
        "<CanAccessTribalstack>": lambda state, player: state.yookaLaylee_can_access_tropics(player), # Wrecked Crow's Nest doesn't spawn until after Tropics entered
        "<ExpandedTribalstackTropics>": lambda state, player: state.yookaLaylee_can_access_tropics_exp(player), # Non-expanded pagie but with different options in expansion
        "<GlacierUpperAccess>": lambda state, player: (
            state.has("Flappy Flight", player)
            or (state.has("Slurp State", player) and (state.has("Tail Twirl", player) or state.has("Glide", player)))
        ),
        "<GlacierLowerAccess>": lambda state, player: state.has("Buddy Slam", player) and state.has("Sonar Shot", player) and state.yookaLaylee_has_requirements("Reptile Rush", player),
        "<GlacierBoss>": lambda state, player: (
            (state.yookaLaylee_has_requirements("<GlacierUpperAccess>", player) or state.yookaLaylee_has_requirements("<GlacierLowerAccess>", player))
            and state.has("Buddy Slam", player) and state.has("Slurp Shot", player)
        ),
        "<MoodymazeEntry>": lambda state, player: state.has("Bubble Buddy", player) or state.has("Lizard Lash", player) or state.has("Flappy Flight", player),
        "<CashinoEntry>": lambda state, player: state.has("Camo Cloak", player) or state.has("Flappy Flight", player),
        "<ExpandedCashino>": lambda state, player: state.yookaLaylee_can_access_cashino_exp(player), # Specifically for Cashino tokens requirements
        "<GalaxyEntry>": lambda state, player: state.has("Flappy Flight", player) or state.has("Glide", player) or state.has("Health Booster", player, 5)
    }

    def yookaLaylee_can_access_HT_hub_entrance(self, player):
        return self.yookaLaylee_has_requirements("<DamagingAbility>", player)

    def yookaLaylee_can_access_HT_hub_B(self, player):
        return (self.yookaLaylee_can_access_HT_hub_entrance(player)
                and (self.has("Reptile Roll", player) or self.has("Flappy Flight", player)) and self.has("Buddy Slam", player))

    def yookaLaylee_can_access_HT_archive(self, player):
        return self.yookaLaylee_can_access_HT_hub_B(player) and self.has("Slurp Shot", player)

    def yookaLaylee_can_access_HT_waterworks(self, player):
        return self.yookaLaylee_can_access_HT_archive(player) and self.has("Buddy Bubble", player) and self.has("Buddy Slam", player)

    def yookaLaylee_can_access_HT_outside(self, player):
        return self.yookaLaylee_can_access_HT_waterworks(player) and (self.has("Lizard Lash", player) or self.has("Flappy Flight", player))

    def yookaLaylee_can_access_HT_finalArea(self, player):
        return self.yookaLaylee_can_access_HT_outside(player) and self.has("Flappy Flight", player)

    def yookaLaylee_can_access_tropics(self, player):
        return (self.has("Pagie", player, 1)
                and self.yookaLaylee_can_access_HT_hub_entrance(player)
                and (self.has("Reptile Roll", player) or self.has("Flappy Flight", player)))

    def yookaLaylee_can_access_tropics_exp(self, player):
        return self.has("Pagie", player, 4) and self.yookaLaylee_can_access_tropics(player)

    def yookaLaylee_can_access_glacier(self, player):
        return (self.has("Pagie", player, 7)
                and self.yookaLaylee_can_access_HT_hub_B(player)
                and (self.has("Glide", player) or self.has("Flappy Flight", player)))

    def yookaLaylee_can_access_glacier_exp(self, player):
        return self.has("Pagie", player, 12) and self.yookaLaylee_can_access_glacier(player)

    def yookaLaylee_can_access_marsh(self, player):
        return (self.has("Pagie", player, 19)
                and self.yookaLaylee_can_access_HT_waterworks(player)
                # TODO Does Buddy Bubble also require Buddy Slam for a switch to open the entrance to get to Marsh book?
                and (self.has("Buddy Bubble", player) or self.has("Lizard Lash", player) or self.has("Flappy Flight", player)))

    def yookaLaylee_can_access_marsh_exp(self, player):
        return self.has("Pagie", player, 27) and self.yookaLaylee_can_access_marsh(player)

    def yookaLaylee_can_access_cashino(self, player):
        return (self.has("Pagie", player, 37)
                and self.yookaLaylee_can_access_HT_outside(player)
                and self.has("Camo Cloak", player))

    def yookaLaylee_can_access_cashino_exp(self, player):
        return self.has("Pagie", player, 48) and self.yookaLaylee_can_access_cashino(player)

    def yookaLaylee_can_access_galaxy(self, player): #Once abilities are items, this will require Flappy Flight
        return self.has("Pagie", player, 60) and self.yookaLaylee_can_access_HT_finalArea(player)

    def yookaLaylee_can_access_galaxy_exp(self, player):
        return self.has("Pagie", player, 75) and self.yookaLaylee_can_access_galaxy(player)

    def yookaLaylee_can_access_end(self, player): # Technically don't need Tail Twirl and Sonar Shield, but the final boss is pretty miserable without it
        return (self.has("Pagie", player, 100)
                and self.yookaLaylee_can_access_HT_finalArea(player)
                and self.yookaLaylee_has_requirements("Sonar Shield", player)
                and self.has("Tail Twirl", player))

    def yookaLaylee_can_get_cashino_token_count(self, player, tokenCount):
        accessibleTokenCount = 0
        for tokenGroup in cashinotokens_table:
            if "abilityRequirements" in tokenGroup:
                if self.yookaLaylee_has_requirements(tokenGroup["abilityRequirements"], player):
                    accessibleTokenCount += tokenGroup["count"]
            else:
                accessibleTokenCount += tokenGroup["count"]
        return accessibleTokenCount >= tokenCount

    def yookaLaylee_has_requirements(self, requirements, player, searchMode = 0):
        if isinstance(requirements, str): # Is ability name
            if requirements in self.yookaLaylee_specialRequirements:
                return self.yookaLaylee_specialRequirements[requirements](self, player)
            elif "<CashinoTokens" in requirements:
                tokenLevel = int(requirements.removeprefix("<CashinoTokens").removesuffix(">"))
                return self.yookaLaylee_can_get_cashino_token_count(player, tokenLevel * 10)
            elif "<(" in requirements:
                itemRequired = requirements.removeprefix("<(").rsplit(")", 1)[0].strip()
                numberRequired = requirements.removeprefix("<(").rsplit(")", 1)[1].strip().removeprefix("x").removesuffix(">")
                return self.has(itemRequired, player, int(numberRequired))
            elif "<" in requirements:
                raise Exception("Unknown special requirement: " + requirements)
            else:
                return self.has(requirements, player)
        elif isinstance(requirements, (list, tuple)): # Is list of requirements, searchMode comes into play here
            checkForAnyRequirement = searchMode == 1 # If searchMode is 0 (default), assume AND
            isValid = not checkForAnyRequirement
            for req in requirements:
                isValid = self.yookaLaylee_has_requirements(req, player)
                if checkForAnyRequirement == isValid:
                    break
            return isValid
        else: # Is object with AND or OR requirement (should never have both)
            if "AND" in requirements:
                if "OR" in requirements:
                    raise Exception(f"Object with both AND and OR present: {str(requirements)}")
                return self.yookaLaylee_has_requirements(requirements["AND"], player)
            elif "OR" in requirements:
                return self.yookaLaylee_has_requirements(requirements["OR"], player, 1)
            else:
                raise Exception(f"Invalid requirements: {str(requirements)}")

def set_rules(world, player):
    regionChecks = {
        "Shipwreck Creek": lambda state: True,
        "Hivory Towers Entrance": lambda state: state.yookaLaylee_can_access_HT_hub_entrance(player),
        "Hivory Towers Hub B": lambda state: state.yookaLaylee_can_access_HT_hub_B(player),
        "Hivory Towers Archive": lambda state: state.yookaLaylee_can_access_HT_archive(player),
        "Hivory Towers Waterworks": lambda state: state.yookaLaylee_can_access_HT_waterworks(player),
        "Hivory Towers Outside (NoFlight)": lambda state: state.yookaLaylee_can_access_HT_outside(player),
        "Hivory Towers Outside (Flight)": lambda state: state.yookaLaylee_can_access_HT_finalArea(player),
        "Tribalstack Tropics": lambda state: state.yookaLaylee_can_access_tropics(player),
        "Expanded Tropics": lambda state: state.yookaLaylee_can_access_tropics_exp(player),
        "Glitterglaze Glacier": lambda state: state.yookaLaylee_can_access_glacier(player),
        "Expanded Glacier": lambda state: state.yookaLaylee_can_access_glacier_exp(player),
        "Moodymaze Marsh": lambda state: state.yookaLaylee_can_access_marsh(player),
        "Expanded Marsh": lambda state: state.yookaLaylee_can_access_marsh_exp(player),
        "Capital Cashino": lambda state: state.yookaLaylee_can_access_cashino(player),
        "Expanded Cashino": lambda state: state.yookaLaylee_can_access_cashino_exp(player),
        "Galleon Galaxy": lambda state: state.yookaLaylee_can_access_galaxy(player),
        "Expanded Galaxy": lambda state: state.yookaLaylee_can_access_galaxy_exp(player),
        "Endgame": lambda state: state.yookaLaylee_can_access_end(player)
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
                canAccess = state.yookaLaylee_has_requirements(location["requiresAbilities"], player)
            return canAccess
        set_rule(locFromWorld, fullLocationCheck)

    # Victory requirement
    world.completion_condition[player] = lambda state: state.has("Victory", player)