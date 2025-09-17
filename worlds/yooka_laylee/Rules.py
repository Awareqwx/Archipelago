from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin
import json
import pkgutil
import re

cashinotokens_table = json.loads(pkgutil.get_data(__name__, "cashinotokens.json").decode())
requiredPagiesPerTomeVanillaOrder = [
    [1, 4],
    [7, 12],
    [19, 27],
    [37, 48],
    [60, 75]
]
randomizedWorldOrder = []

class YookaLayleeLogic(LogicMixin):
    def yookaLaylee_canTailTwirl(self, player):
        return self.has("Tail Twirl", player)
    
    def yookaLaylee_canReptileRoll(self, player):
        return self.has("Reptile Roll", player)
    
    def yookaLaylee_canGlide(self, player):
        return self.has("Glide", player)
    
    def yookaLaylee_canBuddyBubble(self, player):
        return self.has("Buddy Bubble", player)
    
    def yookaLaylee_canCamoCloak(self, player):
        return self.has("Camo Cloak", player)
    
    def yookaLaylee_canFlappyFlight(self, player):
        return self.has("Flappy Flight", player)
    
    def yookaLaylee_canSonarShot(self, player):
        return self.has("Sonar Shot", player)
    
    def yookaLaylee_canSlurpShot(self, player):
        return self.has("Slurp Shot", player)
    
    def yookaLaylee_canBuddySlam(self, player):
        return self.has("Buddy Slam", player)
    
    def yookaLaylee_canSlurpState(self, player):
        return self.has("Slurp State", player)
    
    def yookaLaylee_canLizardLeap(self, player):
        return self.has("Lizard Leap", player)
    
    def yookaLaylee_canLizardLash(self, player):
        return self.has("Lizard Lash", player)

    def yookaLaylee_canSonarSplosion(self, player):
        return self.has("Sonar 'Splosion", player)
    
    def yookaLaylee_canReptileRush(self, player):
        return self.yookaLaylee_canReptileRoll(player) and self.has("Reptile Rush", player)

    def yookaLaylee_canSonarShield(self, player):
        return self.yookaLaylee_canReptileRoll(player) and self.has("Sonar Shield", player)
    
    def yookaLaylee_hasHealthBoosterCount(self, player, count):
        return self.has("Health Booster", player, count)
    
    def yookaLaylee_hasDamagingAbility(self, player):
        return (self.yookaLaylee_canTailTwirl(player)
            or self.yookaLaylee_canBuddySlam(player)
            or self.yookaLaylee_canSonarSplosion(player)
            or self.yookaLaylee_canReptileRush(player)
            or self.yookaLaylee_canSonarShield(player))
    
    def yookaLaylee_checkRequirementsForWorld(self, player, worldIdentifier, expanded = False):
        worldOrderIndex = randomizedWorldOrder.index(worldIdentifier)
        if (self.has("Pagie", player, requiredPagiesPerTomeVanillaOrder[worldOrderIndex][1 if expanded else 0])):
            match worldOrderIndex:
                case 0:
                    return self.yookaLaylee_can_access_HT_hub_entrance(player) and (self.yookaLaylee_canReptileRoll(player) or self.yookaLaylee_canFlappyFlight(player))
                case 1:
                    return self.yookaLaylee_can_access_HT_hub_B(player) and (self.yookaLaylee_canGlide(player) or self.yookaLaylee_canFlappyFlight(player))
                case 2:
                    return self.yookaLaylee_can_access_HT_waterworks(player) and (self.yookaLaylee_canBuddyBubble(player) or self.yookaLaylee_canLizardLash(player) or self.yookaLaylee_canFlappyFlight(player))
                case 3:
                    return self.yookaLaylee_can_access_HT_outside(player) and self.yookaLaylee_canCamoCloak(player)
                case 4:
                    return self.yookaLaylee_can_access_HT_finalArea(player)
        return False

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
        return self.yookaLaylee_checkRequirementsForWorld(player, "TT")

    def yookaLaylee_can_access_tropics_exp(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "TT", True)

    def yookaLaylee_can_access_glacier(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "GG")

    def yookaLaylee_can_access_glacier_exp(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "GG", True)

    def yookaLaylee_can_access_marsh(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "MM")

    def yookaLaylee_can_access_marsh_exp(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "MM", True)

    def yookaLaylee_can_access_cashino(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "CC")

    def yookaLaylee_can_access_cashino_exp(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "CC", True)

    def yookaLaylee_can_access_galaxy(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "GY")

    def yookaLaylee_can_access_galaxy_exp(self, player):
        return self.yookaLaylee_checkRequirementsForWorld(player, "GY", True)

    def yookaLaylee_can_access_end(self, player): # Technically don't need Tail Twirl and Sonar Shield, but the final boss is pretty miserable without it
        return (self.has("Pagie", player, 100) # Pagie count should not affect item placement, since endgame is locked. TODO Verify this.
                and self.yookaLaylee_can_access_HT_finalArea(player)
                and self.yookaLaylee_has_requirements("Sonar Shield", player)
                and self.has("Tail Twirl", player))

    def yookaLaylee_can_get_cashino_token_count(self, player, tokenCount):
        accessibleTokenCount = 0
        for tokenGroup in cashinotokens_table:
            if "requiresAbilities" in tokenGroup:
                if self.yookaLaylee_has_requirements(tokenGroup["requiresAbilities"], player):
                    accessibleTokenCount += tokenGroup["count"]
            else:
                accessibleTokenCount += tokenGroup["count"]
        return accessibleTokenCount >= tokenCount

    def yookaLaylee_has_requirements(self, requirements, player, searchMode = 0):
        if isinstance(requirements, str): # Is ability name
            match requirements:
                case "Reptile Rush":
                    return self.yookaLaylee_canReptileRush(player)
                case "Sonar Shield":
                    return self.yookaLaylee_canSonarShield(player)
                case "<DamagingAbility>":
                    return self.yookaLaylee_hasDamagingAbility(player)
                case "<CanAccessTribalstack>": # Wrecked Crow's Nest doesn't spawn until after Tropics entered
                    return self.yookaLaylee_can_access_tropics(player)
                case "<ExpandedTribalstackTropics>": # Non-expanded pagie but with different options in expansion
                    return self.yookaLaylee_can_access_tropics_exp(player)
                case "<GlacierUpperAccess>":
                    return (self.yookaLaylee_canFlappyFlight(player)
                        or (self.yookaLaylee_canSlurpState(player) and (self.yookaLaylee_canTailTwirl(player) or self.yookaLaylee_canGlide(player))))
                case "<GlacierLowerAccess>":
                    return self.yookaLaylee_canBuddySlam(player) and self.yookaLaylee_canSonarShot(player) and self.yookaLaylee_canReptileRush(player)
                case "<GlacierBoss>":
                    return ((self.yookaLaylee_has_requirements("<GlacierUpperAccess>", player) or self.yookaLaylee_has_requirements("<GlacierLowerAccess>", player))
                        and self.yookaLaylee_canBuddySlam(player) and self.yookaLaylee_canSlurpShot(player))
                case "<MoodymazeEntry>":
                    return self.yookaLaylee_canBuddyBubble(player) or self.yookaLaylee_canLizardLash(player) or self.yookaLaylee_canFlappyFlight(player)
                case "<CashinoEntry>":
                    return self.yookaLaylee_canCamoCloak(player) or self.yookaLaylee_canFlappyFlight(player)
                case "<ExpandedCashino>": # Specifically for Cashino tokens requirements
                    return self.yookaLaylee_can_access_cashino_exp(player)
                case "<GalaxyEntry>":
                    return self.yookaLaylee_canFlappyFlight(player) or self.yookaLaylee_canGlide(player) or self.yookaLaylee_hasHealthBoosterCount(player, 5)
            if "<CashinoTokens" in requirements:
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

def set_rules(world, player, regionOrder):
    global randomizedWorldOrder
    randomizedWorldOrder = regionOrder
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