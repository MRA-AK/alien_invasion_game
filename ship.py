import pygame
from pygame.sprite import Sprite

from resources import resource_path


class Ship(Sprite):
    """Manage the player's ship and its movement."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load(
            str(resource_path("images", "ship.bmp"))
        ).convert()
        self.image.set_colorkey(self.settings.bg_color)
        self.rect = self.image.get_rect()
        self.x = 0.0

        self.moving_right = False
        self.moving_left = False
        self.center_ship()

    def update(self, dt):
        """Move the ship using elapsed seconds while enforcing boundaries."""
        distance = self.settings.ship_speed * dt
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += distance
        if self.moving_left and self.rect.left > 0:
            self.x -= distance

        max_x = self.screen_rect.right - self.rect.width
        self.x = max(0.0, min(self.x, float(max_x)))
        self.rect.x = round(self.x)

    def center_ship(self):
        """Place the ship at the bottom center of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def reset_movement(self):
        """Clear movement flags between game states."""
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
