from Options import Range, Toggle, DefaultOnToggle, Choice

class UseResourcePacks(DefaultOnToggle):
    """Uses Resource Packs to fill out the item pool from Raft. Resource Packs have basic earlygame items such as planks, plastic, or food."""
    displayname = "Use resource packs"

class MinimumResourcePackAmount(Range):
    """The minimum amount of resources available in a resource pack"""
    displayname = "Minimum resource pack amount"
    range_start = 1
    range_end = 15
    default = 1

class MaximumResourcePackAmount(Range):
    """The maximum amount of resources available in a resource pack"""
    displayname = "Maximum resource pack amount"
    range_start = 1
    range_end = 15
    default = 5

class DuplicateItems(Choice):
    """Adds duplicates of items to the item pool if the configured Resource Pack amount
    doesn't have enough to do so. Note that there are not many progression items, and
    selecting Progression may produce many duplicates."""
    displayname = "Duplicate items"
    option_off = 0
    option_progression = 1
    option_non_progression = 2
    option_any = 3

class IslandFrequencyLocations(Choice):
    """Sets where frequencies for story islands are located."""
    displayname = "Frequency locations"
    option_vanilla = 0
    option_random_on_island = 1
    option_progressive = 2
    option_anywhere = 3
    default = 1

class ProgressiveItems(DefaultOnToggle):
    """Makes some items, like the Bow and Arrow, progressive rather than raw unlocks."""
    displayname = "Progressive items"

class BigIslandEarlyCrafting(Toggle):
    """Allows recipes that require items from big islands (eg leather) to lock earlygame items like the Receiver, Bolt, or Smelter."""
    displayname = "Early recipes behind big islands"

class PaddleboardMode(Toggle):
    """Sets later story islands to in logic without an Engine or Steering Wheel. May require lots of paddling. Not recommended."""
    displayname = "Paddleboard Mode"

raft_options = {
    "use_resource_packs": UseResourcePacks,
    "minimum_resource_pack_amount": MinimumResourcePackAmount,
    "maximum_resource_pack_amount": MaximumResourcePackAmount,
    "duplicate_items": DuplicateItems,
    "island_frequency_locations": IslandFrequencyLocations,
    "progressive_items": ProgressiveItems,
    "big_island_early_crafting": BigIslandEarlyCrafting,
    "paddleboard_mode": PaddleboardMode
}
