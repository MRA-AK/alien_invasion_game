import pygame
from pygame.sprite import Sprite

from resources import resource_path


class Alien(Sprite):
    """Represent one alien in the fleet."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load(
            str(resource_path("images", "alien.bmp"))
        ).convert()
        self.image.set_colorkey(self.settings.asset_bg_color)
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return whether the alien has reached either screen edge."""
        return self.rect.right >= self.screen_rect.right or self.rect.left <= 0

    def update(self, dt):
        """Move horizontally according to the fleet direction."""
        self.x += (
            self.settings.alien_speed
            * self.settings.fleet_direction
            * dt
        )
        self.rect.x = round(self.x)
