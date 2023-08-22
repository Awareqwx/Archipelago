from Options import Range, Toggle, DefaultOnToggle, Choice, DeathLink

class FlappyFlightLocation(Choice):
    """Choose where Flappy Flight is put. Flappy Flight opens up many checks and effectively invalidates some abilities like Lizard Leap. "Early" refers to one of the earlygame checks before entering Tribalstack Tropics."""
    display_name = "Flappy Flight location"
    option_forceEarly = 1
    option_allowEarly = 2
    option_vanilla = 3
    option_anywhere = 4
    default = 2

yooka_options = {
    "flappy_flight_location": FlappyFlightLocation,
    "death_link": DeathLink
}
