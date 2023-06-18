from enum import Enum


class Color(Enum):
    """An enum class that represents colors."""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PERFECT = (104, 158, 227, 255)
    GOOD = (124, 208, 139, 255)
    BAD = (227, 158, 104, 255)
    MISS = (227, 111, 105, 255)


class GameState(Enum):
    """An enum class that represents the state of the game."""

    PLAYING = 0
    MAIN_MENU = 1
    SETTINGS_MENU = 2
    PAUSED = 3
    CHART_SELECT_MENU = 4
    DIFFICULTY_SELECT_MENU = 5
    ENDSCREEN = 6
