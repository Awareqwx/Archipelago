from Options import Range, Toggle, DefaultOnToggle

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

class ProgressiveItems(DefaultOnToggle):
    """Makes some items, like the Bow and Arrow, progressive rather than raw unlocks."""
    displayname = "Progressive items"

class ProgressiveFrequencies(DefaultOnToggle):
    """Makes story island frequencies progressive, which generally forces more linear gameplay."""
    displayname = "Progressive frequencies"

class BigIslandEarlyCrafting(Toggle):
    """Allows recipes that require items from big islands (eg leather) to lock earlygame items like the Receiver, Bolt, or Smelter."""
    displayname = "Early recipes behind big islands"

class PaddleboardMode(Toggle):
    """Sets later story islands to in logic without an Engine or Steering Wheel. May require lots of paddling. Not recommended."""
    displayname = "Paddleboard Mode"

options = {
    "use_resource_packs": UseResourcePacks,
    "minimum_resource_pack_amount": MinimumResourcePackAmount,
    "maximum_resource_pack_amount": MaximumResourcePackAmount,
    "progressive_items": ProgressiveItems,
    "progressive_frequencies": ProgressiveFrequencies,
    "big_island_early_crafting": BigIslandEarlyCrafting,
    "paddleboard_mode": PaddleboardMode
}
