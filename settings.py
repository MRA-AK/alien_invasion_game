class Settings:
    """Store static settings and level-dependent gameplay values."""

    def __init__(self):
        # Display settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.frame_rate = 60

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Fleet and difficulty settings.
        self.fleet_drop_speed = 20
        self.speedup_scale = 1.10
        self.score_scale = 1.50

        # Interface colors.
        self.text_color = (25, 35, 55)
        self.accent_color = (40, 130, 210)
        self.button_color = (40, 155, 80)

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Reset settings that change as the player advances."""
        self.ship_speed = 350.0
        self.bullet_speed = 600.0
        self.alien_speed = 70.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Increase movement speeds and scoring for a new level."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
