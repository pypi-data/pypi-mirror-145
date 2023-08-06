"""
Absolute paths of anything that the program needs.
"""

from importlib.resources import path as fpath
from typing import Optional

def file_path(filename: str, subpackage: Optional[str]=None) -> str:
    """
    Returns the absolute path of a file associated with a package or subpackage.
    """

    subpackage_path = f"gamelibgames{f'.{subpackage}' if subpackage else ''}"

    return str(fpath(subpackage_path, filename))

MINE_ICON = file_path("minesweeper_logo.gif", "minesweeper.img.icon")
MINE_FIGURES =  file_path("figures.txt", "minesweeper")
MINE_PROFILES = file_path("color_profiles.txt", "minesweeper")
MINE_MARKED = file_path("marked.wav", "minesweeper.sfx")
MINE_CELL = file_path("uncovered_{cell}.wav", "minesweeper.sfx")
MINE_BTN_UP = file_path("button_up.wav", "minesweeper.sfx")
MINE_BTN_DN = file_path("button_dn.wav", "minesweeper.sfx")
MINE_POPUP = file_path("popup.wav", "minesweeper.sfx")
MINE_BOOM = file_path("boom.wav", "minesweeper.sfx")
MINE_VICTORY = file_path("victory.wav", "minesweeper.sfx")
MINE_NEW_GAME = file_path("new_game.wav", "minesweeper.sfx")