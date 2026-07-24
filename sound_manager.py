import pygame

from resources import resource_path


class SoundManager:
    """Load and play sound effects without making audio mandatory."""

    SOUND_FILES = {
        "laser": "laser.wav",
        "explosion": "explosion.wav",
        "game_over": "game_over.wav",
    }

    def __init__(self):
        self.available = False
        self.muted = False
        self.sounds = {}

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            self.sounds = {
                name: pygame.mixer.Sound(
                    str(resource_path("sounds", filename))
                )
                for name, filename in self.SOUND_FILES.items()
            }
            self.available = True
        except (pygame.error, FileNotFoundError, OSError):
            self.sounds = {}

    def play(self, name):
        """Play a named effect when audio is available and unmuted."""
        if self.available and not self.muted and name in self.sounds:
            self.sounds[name].play()

    def toggle_mute(self):
        """Toggle session mute and return the new muted state."""
        self.muted = not self.muted
        return self.muted
