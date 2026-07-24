import pygame

from ui_fonts import get_ui_font


class Button:
    """Draw and manage a glowing, centered action button."""

    def __init__(self, ai_game, message):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.width, self.height = 270, 70
        self.text_color = (245, 255, 252)
        self.font = get_ui_font(34, bold=True)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.screen_rect.centerx, 465)
        self.update_message(message)

    def update_message(self, message):
        """Render a new label centered on the button."""
        self.message = message
        self.message_image = self.font.render(message.upper(), True, self.text_color)
        self.message_image_rect = self.message_image.get_rect(center=self.rect.center)

    def draw(self):
        """Draw the button with hover feedback, border, and a soft glow."""
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = (
            self.settings.button_hover_color
            if hovered
            else self.settings.button_color
        )

        glow = pygame.Surface((self.width + 28, self.height + 28), pygame.SRCALPHA)
        pygame.draw.rect(
            glow,
            (*color, 42),
            glow.get_rect(),
            border_radius=20,
        )
        self.screen.blit(glow, glow.get_rect(center=self.rect.center))
        pygame.draw.rect(self.screen, color, self.rect, border_radius=12)
        pygame.draw.rect(
            self.screen,
            (175, 255, 225),
            self.rect,
            width=2,
            border_radius=12,
        )
        self.screen.blit(self.message_image, self.message_image_rect)
