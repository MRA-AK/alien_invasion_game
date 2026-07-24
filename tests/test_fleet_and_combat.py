import pygame
import pytest

from bullet import Bullet
from game_stats import GameState


def test_fleet_fills_multiple_rows_and_columns(game):
    x_positions = {alien.rect.x for alien in game.aliens}
    y_positions = {alien.rect.y for alien in game.aliens}

    assert len(game.aliens) > 1
    assert len(x_positions) > 1
    assert len(y_positions) > 1


def test_alien_movement_uses_elapsed_time(game):
    alien = next(iter(game.aliens))
    start_x = alien.x
    alien.update(0.5)

    assert alien.x == pytest.approx(start_x + 35.0)


def test_fleet_reverses_and_drops_at_edge(game):
    alien = max(game.aliens, key=lambda member: member.rect.right)
    alien.rect.right = game.screen.get_rect().right
    alien.x = float(alien.rect.x)
    old_y = {member: member.rect.y for member in game.aliens}

    game._check_fleet_edges()

    assert game.settings.fleet_direction == -1
    assert all(
        member.rect.y == old_y[member] + game.settings.fleet_drop_speed
        for member in game.aliens
    )


def test_collision_scores_and_starts_faster_level(game):
    game._start_game()
    target = next(iter(game.aliens))
    game.aliens = pygame.sprite.Group(target)
    bullet = Bullet(game)
    bullet.rect.center = target.rect.center
    bullet.y = float(bullet.rect.y)
    game.bullets.add(bullet)

    game._update_bullets(0.0)

    assert game.stats.score == 50
    assert game.stats.high_score == 50
    assert game.stats.level == 2
    assert game.settings.alien_speed == pytest.approx(77.0)
    assert game.aliens


def test_multi_alien_collision_scores_every_destroyed_alien(game):
    game._start_game()
    aliens = list(game.aliens)[:2]
    for alien in aliens:
        alien.rect.center = (300, 300)
        alien.x = float(alien.rect.x)
    game.aliens = pygame.sprite.Group(*aliens)
    bullet = Bullet(game)
    bullet.rect.center = (300, 300)
    bullet.y = float(bullet.rect.y)
    game.bullets.add(bullet)

    game._update_bullets(0.0)

    assert game.stats.score == 100


def test_three_hits_end_game_and_restart_retains_high_score(game):
    game._start_game()
    game.stats.add_score(500)

    game._ship_hit()
    assert game.stats.ships_left == 2
    assert game.stats.state is GameState.PLAYING
    game._ship_hit()
    assert game.stats.ships_left == 1
    game._ship_hit()

    assert game.stats.ships_left == 0
    assert game.stats.state is GameState.GAME_OVER
    assert game.play_button.message == "Play Again"

    game._start_game()
    assert game.stats.state is GameState.PLAYING
    assert game.stats.ships_left == 3
    assert game.stats.score == 0
    assert game.stats.level == 1
    assert game.stats.high_score == 500
    assert game.settings.alien_points == 50
    assert not game.bullets


def test_alien_reaching_bottom_costs_one_life(game):
    game._start_game()
    alien = next(iter(game.aliens))
    game.aliens = pygame.sprite.Group(alien)
    alien.rect.bottom = game.screen.get_rect().bottom

    game._update_aliens(0.0)

    assert game.stats.ships_left == 2


def test_pause_state_toggles_without_resetting_session(game):
    game._start_game()
    game.stats.score = 125
    game._toggle_pause()
    assert game.stats.state is GameState.PAUSED
    assert not game.ship.moving_left
    assert not game.ship.moving_right

    game._toggle_pause()
    assert game.stats.state is GameState.PLAYING
    assert game.stats.score == 125
