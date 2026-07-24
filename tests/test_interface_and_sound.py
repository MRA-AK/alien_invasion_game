import pygame

from game_stats import GameState
from scoreboard import Scoreboard
from sound_manager import SoundManager


def test_scoreboard_formats_values_and_lives(game):
    game.stats.score = 12_345
    game.stats.high_score = 98_765
    game.stats.level = 4
    game.stats.ships_left = 2
    game.scoreboard.refresh()

    assert Scoreboard.format_score(12_345) == "12,345"
    assert game.scoreboard.score_text == "Score 12,345"
    assert game.scoreboard.high_score_text == "High Score 98,765"
    assert game.scoreboard.level_text == "Level 4"
    assert len(game.scoreboard.life_rects) == 2


def test_every_state_renders_headlessly(game):
    for state in GameState:
        game.stats.state = state
        game._update_screen()


def test_play_button_starts_menu_and_game_over(game):
    center = game.play_button.rect.center
    game._check_play_button(center)
    assert game.stats.state is GameState.PLAYING

    game.stats.state = GameState.GAME_OVER
    game._check_play_button(center)
    assert game.stats.state is GameState.PLAYING


def test_sound_manager_can_mute_loaded_sounds():
    manager = SoundManager()
    assert manager.muted is False
    assert manager.toggle_mute() is True
    assert manager.toggle_mute() is False


def test_sound_manager_survives_mixer_failure(monkeypatch):
    monkeypatch.setattr(pygame.mixer, "get_init", lambda: None)

    def fail_init():
        raise pygame.error("No audio device")

    monkeypatch.setattr(pygame.mixer, "init", fail_init)
    manager = SoundManager()

    assert manager.available is False
    manager.play("laser")
