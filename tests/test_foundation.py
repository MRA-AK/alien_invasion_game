from pathlib import Path
import sys

import pytest

from resources import resource_path
from settings import Settings


def test_dynamic_settings_reset_and_scale():
    settings = Settings()
    settings.increase_speed()

    assert settings.ship_speed == pytest.approx(385.0)
    assert settings.bullet_speed == pytest.approx(660.0)
    assert settings.alien_speed == pytest.approx(77.0)
    assert settings.alien_points == 75

    settings.initialize_dynamic_settings()
    assert settings.ship_speed == 350.0
    assert settings.alien_points == 50
    assert settings.fleet_direction == 1


def test_resource_path_uses_bundle_root(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)

    assert resource_path("images", "ship.bmp") == (
        Path(tmp_path) / "images" / "ship.bmp"
    )


def test_ship_movement_is_delta_timed_and_bounded(game):
    game.ship.moving_right = True
    start_x = game.ship.x
    game.ship.update(0.5)
    assert game.ship.x == pytest.approx(start_x + 175.0)

    game.ship.x = float(game.ship.screen_rect.right - game.ship.rect.width)
    game.ship.rect.x = round(game.ship.x)
    game.ship.update(1.0)
    assert game.ship.rect.right == game.ship.screen_rect.right

    game.ship.moving_right = False
    game.ship.moving_left = True
    game.ship.x = 0.0
    game.ship.rect.x = 0
    game.ship.update(1.0)
    assert game.ship.rect.left == 0


def test_bullet_limit_and_cleanup(game):
    game._start_game()
    for _ in range(game.settings.bullets_allowed + 2):
        game._fire_bullet()

    assert len(game.bullets) == game.settings.bullets_allowed

    for bullet in game.bullets:
        bullet.y = -float(bullet.rect.height)
        bullet.rect.y = round(bullet.y)
    game._update_bullets(0.0)
    assert not game.bullets
