from enum import Enum, auto


class GameState(Enum):
    """Possible top-level game states."""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class GameStats:
    """Track state and scoring for Alien Invasion."""

    def __init__(self, settings):
        self.settings = settings
        self.high_score = 0
        self.state = GameState.MENU
        self.reset_stats()

    def reset_stats(self):
        """Reset values that change during one game session."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def add_score(self, points):
        """Add points and update the process-lifetime high score."""
        self.score += points
        self.high_score = max(self.high_score, self.score)
