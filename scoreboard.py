import pygame

from ui_fonts import get_ui_font


class Scoreboard:
    """Render a compact sci-fi HUD for score, level, and lives."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ship_image = ai_game.ship.image

        self.label_font = get_ui_font(15, bold=True)
        self.value_font = get_ui_font(30, bold=True, monospace=True)
        self.level_font = get_ui_font(27, bold=True)
        self.panel_rect = pygame.Rect(18, 14, self.screen_rect.width - 36, 94)
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

    def _label(self, text):
        return self.label_font.render(text, True, self.settings.muted_text_color)

    def _value(self, text, color=None):
        return self.value_font.render(
            text, True, color or self.settings.text_color
        )

    def _prepare_score(self):
        value = self.format_score(self.stats.score)
        self.score_text = f"Score {value}"
        self.score_label = self._label("SCORE")
        self.score_image = self._value(value, self.settings.accent_color)
        self.score_label_rect = self.score_label.get_rect(right=1150, top=28)
        self.score_rect = self.score_image.get_rect(right=1150, top=49)

    def _prepare_high_score(self):
        value = self.format_score(self.stats.high_score)
        self.high_score_text = f"High Score {value}"
        self.high_score_label = self._label("HIGH SCORE")
        self.high_score_image = self._value(value)
        self.high_score_label_rect = self.high_score_label.get_rect(
            centerx=520, top=28
        )
        self.high_score_rect = self.high_score_image.get_rect(
            centerx=520, top=49
        )

    def _prepare_level(self):
        self.level_text = f"Level {self.stats.level}"
        self.level_label = self._label("LEVEL")
        self.level_image = self.level_font.render(
            f"{self.stats.level:02d}", True, self.settings.secondary_color
        )
        self.level_label_rect = self.level_label.get_rect(centerx=810, top=28)
        self.level_rect = self.level_image.get_rect(centerx=810, top=50)

    def _prepare_ships(self):
        self.ships_label = self._label("SHIPS")
        self.ships_label_rect = self.ships_label.get_rect(left=42, top=28)
        icon_size = (38, 30)
        # Nearest-neighbor scaling preserves the bitmap's exact color key.
        self.ship_icon = pygame.transform.scale(self.ship_image, icon_size)
        self.ship_icon.set_colorkey(self.settings.asset_bg_color)
        self.life_rects = []
        for index in range(self.stats.ships_left):
            rect = self.ship_icon.get_rect()
            rect.x = 42 + index * (icon_size[0] + 9)
            rect.y = 56
            self.life_rects.append(rect)

    def show(self):
        """Draw the HUD panel and current values."""
        pygame.draw.rect(
            self.screen,
            self.settings.panel_color,
            self.panel_rect,
            border_radius=14,
        )
        pygame.draw.rect(
            self.screen,
            self.settings.panel_border_color,
            self.panel_rect,
            width=2,
            border_radius=14,
        )
        pygame.draw.line(
            self.screen,
            self.settings.accent_color,
            (36, self.panel_rect.bottom - 5),
            (self.panel_rect.right - 18, self.panel_rect.bottom - 5),
            2,
        )
        for x in (270, 700, 910):
            pygame.draw.line(
                self.screen,
                self.settings.panel_border_color,
                (x, 30),
                (x, 90),
            )

        self.screen.blit(self.ships_label, self.ships_label_rect)
        self.screen.blit(self.high_score_label, self.high_score_label_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_label, self.level_label_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.score_label, self.score_label_rect)
        self.screen.blit(self.score_image, self.score_rect)
        for rect in self.life_rects:
            self.screen.blit(self.ship_icon, rect)
