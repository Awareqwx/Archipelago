from Options import Range, Toggle, DefaultOnToggle, Choice, DeathLink

class ForceLocalFirstItem(Toggle):
    """If enabled, forces an ability that can deal damage into your world as the first location you can check (where Trowzer teaches you Tail Twirl). Otherwise, it will be filled into any location that is reachable from the beginning of any game."""
    display_name = "Force local first abilitiy"

class PreventTropicsBK(DefaultOnToggle):
    """If enabled, forces either Reptile Roll or Flappy Flight into your world in a location accessible before Tribalstack Tropics. If disabled, these abilities may be placed anywhere."""
    display_name = "Prevent Tropics BK"

class FlappyFlightLocation(Choice):
    """Choose where Flappy Flight is put. Flappy Flight opens up many checks and effectively invalidates some abilities like Lizard Leap. "Early" refers to one of the earlygame checks before entering Tribalstack Tropics."""
    display_name = "Flappy Flight Location"
    option_force_early = 1
    option_allow_early = 2
    option_vanilla = 3
    option_anywhere = 4
    default = 2

class PagiesRequiredForCapitalB(Range):
    """The amount of pagies required to face Capital B. Note that this does NOT guarantee you will be able to access Capital B's office at a particular time, as there are still ability requirements to progress up to Capital B's office in the first place. There are a total of 145 pagies in the game."""
    display_name = "Pagies Required for Capital B"
    range_start = 0
    range_end = 145
    default = 100

class GrandTomeRandomization(Toggle):
    """If enabled, randomizes the order of the Grand Tome worlds. This does not change the location of the Grand Tomes within Hivory Towers or the cost of the Grand Tomes, only the world you go to when entering a Grand Tome. Galleon Galaxy will never be randomized in place of Tribalstack Tropics."""
    display_name = "Randomize Grand Tome World Order"

class DisableQuizzes(Toggle):
    """If enabled, causes the quizzes to be completely skipped."""
    display_name = "Disable Quizzes"

yooka_options = {
    "force_local_first_item": ForceLocalFirstItem,
    "prevent_tropics_bk": PreventTropicsBK,
    "flappy_flight_location": FlappyFlightLocation,
    "capital_b_pagie_count": PagiesRequiredForCapitalB,
    "randomize_grand_tomes": GrandTomeRandomization,
    "disable_quizzes": DisableQuizzes,
    "death_link": DeathLink
}
