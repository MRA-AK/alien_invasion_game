"""Cross-platform font selection for the game's interface."""

import pygame.font


DISPLAY_FONTS = (
    "bahnschrift",
    "segoeui",
    "dejavusans",
    "arial",
)
MONO_FONTS = (
    "cascadiamono",
    "consolas",
    "dejavusansmono",
    "couriernew",
)


def get_ui_font(size, *, bold=False, monospace=False):
    """Return the first installed font in the preferred fallback stack."""
    candidates = MONO_FONTS if monospace else DISPLAY_FONTS
    font_path = pygame.font.match_font(
        ",".join(candidates), bold=bold
    )
    font = pygame.font.Font(font_path, size) if font_path else pygame.font.Font(None, size)
    font.set_bold(bold)
    return font
