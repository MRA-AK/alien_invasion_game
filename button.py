import pygame.font


class Button:
    """Draw and manage a centered action button."""

    def __init__(self, ai_game, message):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.width, self.height = 240, 64
        self.button_color = self.settings.button_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 42)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.update_message(message)

    def update_message(self, message):
        """Render a new label centered on the button."""
        self.message = message
        self.message_image = self.font.render(
            message, True, self.text_color, self.button_color
        )
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw(self):
        """Draw the button and its label."""
        pygame.draw.rect(self.screen, self.button_color, self.rect, border_radius=8)
        self.screen.blit(self.message_image, self.message_image_rect)
