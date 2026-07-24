import random
import sys

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameState, GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from sound_manager import SoundManager
from ui_fonts import get_ui_font


class AlienInvasion:
    """Manage game resources, behavior, and the main loop."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        self.stars = self._create_starfield()

        self.stats = GameStats(self.settings)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.sounds = SoundManager()
        self.scoreboard = Scoreboard(self)
        self.play_button = Button(self, "Play")

        self.title_font = get_ui_font(86, bold=True)
        self.overlay_font = get_ui_font(56, bold=True)
        self.score_font = get_ui_font(38, bold=True, monospace=True)
        self.help_font = get_ui_font(24, bold=True)
        self.eyebrow_font = get_ui_font(17, bold=True)

    def run_game(self):
        """Run the main event/update/render loop."""
        while True:
            dt = min(self.clock.tick(self.settings.frame_rate) / 1000.0, 0.05)
            self._check_events()

            if self.stats.state is GameState.PLAYING:
                self.ship.update(dt)
                self._update_bullets(dt)
                self._update_aliens(dt)

            self._update_screen()

    def _check_events(self):
        """Respond to keyboard, mouse, and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._check_play_button(event.pos)

    def _check_keydown_events(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = True
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._quit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_RETURN:
            if self.stats.state in (GameState.MENU, GameState.GAME_OVER):
                self._start_game()
        elif event.key in (pygame.K_p, pygame.K_ESCAPE):
            self._toggle_pause()
        elif event.key == pygame.K_m:
            self.sounds.toggle_mute()

    def _check_keyup_events(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = False
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = False

    def _check_play_button(self, mouse_position):
        if (
            self.stats.state in (GameState.MENU, GameState.GAME_OVER)
            and self.play_button.rect.collidepoint(mouse_position)
        ):
            self._start_game()

    def _start_game(self):
        """Start a fresh session while retaining the process high score."""
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.state = GameState.PLAYING
        self.bullets.empty()
        self.aliens.empty()
        self.ship.center_ship()
        self.ship.reset_movement()
        self._create_fleet()
        self.scoreboard.refresh()
        self.play_button.update_message("Play")
        pygame.mouse.set_visible(False)

    def _toggle_pause(self):
        if self.stats.state is GameState.PLAYING:
            self.stats.state = GameState.PAUSED
            self.ship.reset_movement()
            pygame.mouse.set_visible(True)
        elif self.stats.state is GameState.PAUSED:
            self.stats.state = GameState.PLAYING
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        if (
            self.stats.state is GameState.PLAYING
            and len(self.bullets) < self.settings.bullets_allowed
        ):
            self.bullets.add(Bullet(self))
            self.sounds.play("laser")

    def _update_bullets(self, dt):
        self.bullets.update(dt)
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        destroyed = sum(len(hit_aliens) for hit_aliens in collisions.values())
        if destroyed:
            self.stats.add_score(self.settings.alien_points * destroyed)
            self.scoreboard.refresh()
            self.sounds.play("explosion")

        if not self.aliens:
            self.bullets.empty()
            self.stats.level += 1
            self.settings.increase_speed()
            self._create_fleet()
            self.scoreboard.refresh()

    def _update_aliens(self, dt):
        self._check_fleet_edges()
        self.aliens.update(dt)

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        elif self._aliens_reached_bottom():
            self._ship_hit()

    def _check_fleet_edges(self):
        if any(alien.check_edges() for alien in self.aliens.sprites()):
            for alien in self.aliens.sprites():
                alien.rect.y += self.settings.fleet_drop_speed
            self.settings.fleet_direction *= -1

    def _aliens_reached_bottom(self):
        screen_rect = self.screen.get_rect()
        return any(
            alien.rect.bottom >= screen_rect.bottom
            for alien in self.aliens.sprites()
        )

    def _ship_hit(self):
        """Handle a fleet collision or an alien reaching the bottom."""
        self.stats.ships_left -= 1
        self.ship.reset_movement()
        self.scoreboard.refresh()

        if self.stats.ships_left <= 0:
            self.stats.state = GameState.GAME_OVER
            self.play_button.update_message("Play Again")
            pygame.mouse.set_visible(True)
            self.sounds.play("game_over")
            return

        self.sounds.play("explosion")
        self.bullets.empty()
        self.aliens.empty()
        self.ship.center_ship()
        self._create_fleet()

    def _create_fleet(self):
        """Create a fleet sized to the available screen area."""
        sample = Alien(self)
        alien_width, alien_height = sample.rect.size
        available_x = self.settings.screen_width - 2 * alien_width
        columns = max(1, available_x // (2 * alien_width))

        available_y = (
            self.settings.screen_height
            - self.settings.fleet_top
            - 2 * alien_height
            - self.ship.rect.height
        )
        rows = max(1, available_y // (2 * alien_height))

        for row in range(rows):
            for column in range(columns):
                self._create_alien(column, row)

    def _create_alien(self, column, row):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = float(alien_width + 2 * alien_width * column)
        alien.rect.x = round(alien.x)
        alien.rect.y = self.settings.fleet_top + 2 * alien_height * row
        self.aliens.add(alien)

    def _create_starfield(self):
        """Create a stable procedural starfield without external assets."""
        randomizer = random.Random(1978)
        stars = []
        colors = ((76, 115, 160), (106, 159, 205), (194, 226, 255))
        for _ in range(105):
            stars.append(
                (
                    randomizer.randrange(self.settings.screen_width),
                    randomizer.randrange(self.settings.screen_height),
                    randomizer.choice((1, 1, 1, 2)),
                    randomizer.choice(colors),
                )
            )
        return stars

    def _draw_starfield(self):
        for x, y, radius, color in self.stars:
            pygame.draw.circle(self.screen, color, (x, y), radius)

    def _draw_centered_text(
        self, text, font, y, color=None, *, shadow=False
    ):
        color = color or self.settings.text_color
        image = font.render(text, True, color)
        rect = image.get_rect(center=(self.screen.get_rect().centerx, y))
        if shadow:
            shadow_image = font.render(text, True, (0, 0, 0))
            self.screen.blit(shadow_image, rect.move(4, 6))
        self.screen.blit(image, rect)

    def _draw_overlay(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((3, 8, 20, 224))
        self.screen.blit(overlay, (0, 0))

    def _draw_info_panel(self, rect):
        pygame.draw.rect(
            self.screen,
            (*self.settings.panel_color, 235),
            rect,
            border_radius=14,
        )
        pygame.draw.rect(
            self.screen,
            self.settings.panel_border_color,
            rect,
            width=2,
            border_radius=14,
        )

    def _draw_menu(self):
        self._draw_overlay()
        self._draw_centered_text(
            "ALIEN INVASION",
            self.title_font,
            185,
            self.settings.accent_color,
            shadow=True,
        )
        self._draw_centered_text(
            "DEFEND THE LAST ORBIT",
            self.eyebrow_font,
            246,
            self.settings.secondary_color,
        )
        controls_panel = pygame.Rect(335, 285, 530, 110)
        self._draw_info_panel(controls_panel)
        self._draw_centered_text(
            "MOVE  LEFT / RIGHT  •  A / D        FIRE  SPACE",
            self.help_font,
            322,
        )
        self._draw_centered_text(
            "PAUSE  P / ESC        MUTE  M        QUIT  Q",
            self.eyebrow_font,
            365,
            self.settings.muted_text_color,
        )
        self.play_button.draw()

    def _draw_paused(self):
        self._draw_overlay()
        panel = pygame.Rect(340, 255, 520, 245)
        self._draw_info_panel(panel)
        self._draw_centered_text(
            "PAUSED",
            self.overlay_font,
            325,
            self.settings.accent_color,
            shadow=True,
        )
        mute_text = "Muted" if self.sounds.muted else "Sound on"
        self._draw_centered_text(
            f"P / ESC TO CONTINUE    •    {mute_text.upper()}",
            self.help_font,
            405,
            self.settings.muted_text_color,
        )

    def _draw_game_over(self):
        self._draw_overlay()
        panel = pygame.Rect(335, 205, 530, 340)
        self._draw_info_panel(panel)
        self._draw_centered_text(
            "GAME OVER",
            self.overlay_font,
            275,
            self.settings.danger_color,
            shadow=True,
        )
        final_score = Scoreboard.format_score(self.stats.score)
        self._draw_centered_text(
            "FINAL SCORE", self.eyebrow_font, 335, self.settings.muted_text_color
        )
        self._draw_centered_text(
            final_score, self.score_font, 375, self.settings.accent_color
        )
        self.play_button.draw()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._draw_starfield()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.scoreboard.show()

        if self.stats.state is GameState.MENU:
            self._draw_menu()
        elif self.stats.state is GameState.PAUSED:
            self._draw_paused()
        elif self.stats.state is GameState.GAME_OVER:
            self._draw_game_over()

        pygame.display.flip()

    @staticmethod
    def _quit():
        pygame.quit()
        raise SystemExit


def main():
    """Run the game, or initialize and render once for release smoke tests."""
    game = AlienInvasion()
    if "--smoke-test" in sys.argv:
        game._update_screen()
        pygame.event.pump()
        pygame.quit()
        return
    game.run_game()


if __name__ == "__main__":
    main()
