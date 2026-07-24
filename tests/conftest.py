import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
import pytest

from alien_invasion import AlienInvasion


@pytest.fixture
def game():
    """Provide a real game instance without entering the main loop."""
    pygame.quit()
    instance = AlienInvasion()
    yield instance
    pygame.quit()
