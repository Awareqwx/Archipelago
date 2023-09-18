from Options import Range, Toggle, DefaultOnToggle, Choice, DeathLink

class ForceLocalFirstItem(Toggle):
    """If enabled, forces an ability that can deal damage into your world as the first location you can check (where Trowzer teaches you Tail Twirl). Otherwise, it will be filled into any location that is reachable from the beginning of any game."""
    display_name = "Force local first abilitiy"

class PreventTropicsBK(DefaultOnToggle):
    """If enabled, forces either Reptile Roll or Flappy Flight into your world in a location accessible before Tribalstack Tropics. If disabled, these abilities may be placed anywhere."""
    display_name = "Prevent Tropics BK"

class FlappyFlightLocation(Choice):
    """Choose where Flappy Flight is put. Flappy Flight opens up many checks and effectively invalidates some abilities like Lizard Leap. "Early" refers to one of the earlygame checks before entering Tribalstack Tropics."""
    display_name = "Flappy Flight location"
    option_force_early = 1
    option_allow_early = 2
    option_vanilla = 3
    option_anywhere = 4
    default = 2

yooka_options = {
    "force_local_first_item": ForceLocalFirstItem,
    "prevent_tropics_bk": PreventTropicsBK,
    "flappy_flight_location": FlappyFlightLocation,
    "death_link": DeathLink
}
