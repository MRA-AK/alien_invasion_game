import pygame.font


class Scoreboard:
    """Render score, high score, level, and remaining lives."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ship_image = ai_game.ship.image
        self.font = pygame.font.SysFont(None, 36)
        self.refresh()

    @staticmethod
    def format_score(value):
        """Format a numeric score with thousands separators."""
        return f"{value:,}"

    def refresh(self):
        """Rebuild every HUD element after a statistics change."""
        self._prepare_score()
        self._prepare_high_score()
        self._prepare_level()
        self._prepare_ships()

    def _render(self, text):
        return self.font.render(
            text, True, self.settings.text_color, self.settings.bg_color
        )

    def _prepare_score(self):
        self.score_text = f"Score {self.format_score(self.stats.score)}"
        self.score_image = self._render(self.score_text)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 24
        self.score_rect.top = 18

    def _prepare_high_score(self):
        value = self.format_score(self.stats.high_score)
        self.high_score_text = f"High Score {value}"
        self.high_score_image = self._render(self.high_score_text)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 18

    def _prepare_level(self):
        self.level_text = f"Level {self.stats.level}"
        self.level_image = self._render(self.level_text)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 8

    def _prepare_ships(self):
        icon_size = (38, 30)
        self.ship_icon = pygame.transform.smoothscale(self.ship_image, icon_size)
        self.life_rects = []
        for index in range(self.stats.ships_left):
            rect = self.ship_icon.get_rect()
            rect.x = 20 + index * (icon_size[0] + 8)
            rect.y = 18
            self.life_rects.append(rect)

    def show(self):
        """Draw the current HUD."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        for rect in self.life_rects:
            self.screen.blit(self.ship_icon, rect)
