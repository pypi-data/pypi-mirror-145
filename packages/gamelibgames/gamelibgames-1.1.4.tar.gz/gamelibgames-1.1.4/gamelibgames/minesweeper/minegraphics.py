from .. import gamelib
from . import minefiles

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from .minesweeper import MinesweeperGame

THEME = "DEFAULT"
"""
Can select between:

* DEFAULT - The vey common one
"""

PROFILE = minefiles.map_color_profiles()[THEME]

FIGURES = minefiles.map_figures()

def draw_GUI(game: 'MinesweeperGame') -> None:
    """
    Draws all of the elements of the Graphic User Interface.
    """

    gamelib.draw_rectangle(0, 0, game.width + 50, game.gui_size, width=(game.width // 300), outline=PROFILE["GUI_OUTLINE_1"], fill=PROFILE["GUI_1"])

    gamelib.draw_rectangle(game.width * 0.65,
                           0,
                           game.width * 0.75,
                           game.gui_size,
                           outline=PROFILE["GUI_OUTLINE_1"], fill=PROFILE["GUI_2"])

    gamelib.draw_text(f"X\n{game.grid_x}",
                      game.width * 0.7,
                      (game.gui_size / 2),
                      justify='c', anchor='c',
                      size=(game.width // 40),
                      fill=PROFILE["GUI_TEXT"])

    gamelib.draw_rectangle(game.width * 0.85,
                           0,
                           game.width * 0.95,
                           game.gui_size,
                           outline=PROFILE["GUI_OUTLINE_1"], fill=PROFILE["GUI_2"])

    gamelib.draw_text(f"Y\n{game.grid_y}",
                      game.width * 0.9,
                      (game.gui_size / 2),
                      justify='c', anchor='c',
                      size=(game.width // 40),
                      fill=PROFILE["GUI_TEXT"])

    gamelib.draw_rectangle(game.width * 0.25,
                           0,
                           game.width * 0.35,
                           game.gui_size,
                           outline=PROFILE["GUI_OUTLINE_1"], fill=PROFILE["GUI_2"])

    gamelib.draw_text(f"Mines:\n{game.mines if game.mines > 0 else 'Auto'}",
                      game.width * 0.3,
                      (game.gui_size / 2),
                      justify='c', anchor='c',
                      size=(game.width // 40),
                      fill=PROFILE["GUI_TEXT"])

def draw_grid(game: 'MinesweeperGame') -> None:
    """
    Draws the game grid.
    """

    cols, rows = game.dimensions()

    extra_space = game.cell_size / 24

    for i in range(cols + 1):

        gamelib.draw_line(game.cell_size * i,
                          game.gui_size,
                          game.cell_size * i,
                          game.height,
                          width=(game.cell_size // 10), fill=PROFILE["CELL_COLOR_3"])

    for j in range(rows + 1):

        gamelib.draw_line(0,
                          (game.cell_size * j) + game.gui_size,
                          game.width,
                          (game.cell_size * j) + game.gui_size,
                          width=(game.cell_size // 10), fill=PROFILE["CELL_COLOR_3"])

    for y in range(rows):

        for x in range(cols):

            cell = game.grid[y][x]

            gamelib.draw_rectangle((game.cell_size * x) + extra_space,
                                   (game.cell_size * y) + game.gui_size + extra_space,
                                   (game.cell_size * (x + 1)) - extra_space,
                                   (game.cell_size * (y + 1)) + game.gui_size - extra_space,
                                   outline=PROFILE["CELL_OUTLINE"], fill=PROFILE["CELL_COLOR_1" if cell is not game.loser_cell else "LOSER_CELL"])

            if cell.is_hidden:

                gamelib.draw_rectangle(game.cell_size * x,
                                      (game.cell_size * y) + game.gui_size,
                                      game.cell_size * (x + 1) - extra_space,
                                      (game.cell_size * y) + game.gui_size + (extra_space * 1.5),
                                      outline=PROFILE["CELL_OUTLINE"], fill=PROFILE["CELL_COLOR_2"])

                gamelib.draw_rectangle(game.cell_size * x,
                                      (game.cell_size * y) + game.gui_size,
                                      (game.cell_size * x) + (extra_space * 1.5),
                                      (game.cell_size * (y + 1)) + game.gui_size - extra_space,
                                      outline=PROFILE["CELL_OUTLINE"], fill=PROFILE["CELL_COLOR_2"])

                if cell.state == 1: # is flagged

                    draw_flag(game, x, y)

                elif cell.state == 2: # dunno

                    draw_dunno(game, x, y)

            else:

                if cell.value == 'X':

                    draw_mine(game, x, y)

                elif not cell.value in (0, ''):

                    # gamelib.draw_text(str(cell.value), (game.cell_size * (x + 0.5)), (game.cell_size * (y + 0.5)) + game.gui_size, justify='c', anchor='c', fill=PROFILE[f"NUMBER_{cell.value}"])
                    draw_number(game, x, y, cell.value)

def draw_flag(game: 'MinesweeperGame', x: int, y: int) -> None:
    """
    Draws the flag if the indicated cell is flagged.
    """

    extra_space = game.cell_size / 10

    # Post
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 2),
                           (game.cell_size * (y + 1)) + game.gui_size - (extra_space * 2.5),
                           (game.cell_size * (x + 1)) - (extra_space * 2),
                           (game.cell_size * (y + 1)) + game.gui_size - extra_space,
                           outline=PROFILE["FLAG_OUTLINE"], fill=PROFILE["FLAG_2"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 3.5),
                          (game.cell_size * (y + 1)) + game.gui_size - (extra_space * 3),
                          (game.cell_size * (x + 1)) - (extra_space * 3.5),
                          (game.cell_size * (y + 1)) + game.gui_size - (extra_space * 2.5),
                          outline=PROFILE["FLAG_OUTLINE"], fill=PROFILE["FLAG_2"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 4.5),
                          (game.cell_size * (y + 0.5)) + game.gui_size,
                          (game.cell_size * (x + 1)) - (extra_space * 4.5),
                          (game.cell_size * (y + 1)) + game.gui_size - (extra_space * 3),
                          outline=PROFILE["FLAG_OUTLINE"], fill=PROFILE["FLAG_2"])

    # Flag
    gamelib.draw_rectangle((game.cell_size * (x + 0.5)) - extra_space,
                           (game.cell_size * y) + game.gui_size + (extra_space * 2),
                           (game.cell_size * (x + 1)) - (extra_space * 4.5),
                           (game.cell_size * (y + 0.5)) + game.gui_size,
                           outline=PROFILE["FLAG_OUTLINE"], fill=PROFILE["FLAG_1"])

    gamelib.draw_rectangle((game.cell_size * (x + 0.5)) - (extra_space * 2.5),
                           (game.cell_size * y) + game.gui_size + (extra_space * 2.5),
                           (game.cell_size * (x + 0.5)) - extra_space,
                           (game.cell_size * (y + 0.5)) + game.gui_size - (extra_space * 0.8),
                           outline=PROFILE["FLAG_OUTLINE"], fill=PROFILE["FLAG_1"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 1.5),
                           (game.cell_size * y) + game.gui_size + (extra_space * 3),
                           (game.cell_size * (x + 0.5)) - (extra_space * 2.5),
                           (game.cell_size * (y + 0.5)) + game.gui_size - (extra_space * 1.3),
                           outline=PROFILE["FLAG_OUTLINE"], fill=PROFILE["FLAG_1"])

def draw_dunno(game: 'MinesweeperGame', x: int, y: int) -> None:
    """
    Draws a question mark to show that a cell has said symbol.
    """

    extra_space = game.cell_size / 13

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 3),
                           (game.cell_size * y) + game.gui_size + (extra_space * 3),
                           (game.cell_size * x) + (extra_space * 5),
                           (game.cell_size * y) + game.gui_size + (extra_space * 6),
                            outline=PROFILE["DUNNO_OUTLINE"], fill=PROFILE["DUNNO_1"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 4),
                           (game.cell_size * y) + game.gui_size + (extra_space * 2),
                           (game.cell_size * x) + (extra_space * 9),
                           (game.cell_size * y) + game.gui_size + (extra_space * 3),
                            outline=PROFILE["DUNNO_OUTLINE"], fill=PROFILE["DUNNO_1"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                           (game.cell_size * y) + game.gui_size + (extra_space * 3),
                           (game.cell_size * x) + (extra_space * 10),
                           (game.cell_size * y) + game.gui_size + (extra_space * 7),
                            outline=PROFILE["DUNNO_OUTLINE"], fill=PROFILE["DUNNO_1"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 7),
                           (game.cell_size * y) + game.gui_size + (extra_space * 6),
                           (game.cell_size * x) + (extra_space * 8),
                           (game.cell_size * y) + game.gui_size + (extra_space * 7),
                            outline=PROFILE["DUNNO_OUTLINE"], fill=PROFILE["DUNNO_1"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 6),
                           (game.cell_size * y) + game.gui_size + (extra_space * 7),
                           (game.cell_size * x) + (extra_space * 8),
                           (game.cell_size * y) + game.gui_size + (extra_space * 9),
                            outline=PROFILE["DUNNO_OUTLINE"], fill=PROFILE["DUNNO_1"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 6),
                           (game.cell_size * y) + game.gui_size + (extra_space * 10),
                           (game.cell_size * x) + (extra_space * 8),
                           (game.cell_size * y) + game.gui_size + (extra_space * 12),
                            outline=PROFILE["DUNNO_OUTLINE"], fill=PROFILE["DUNNO_1"])

def draw_mine(game: 'MinesweeperGame', x: int, y: int) -> None:
    """
    Draws a mine if the cell indicated by the parameter coordiantes has it.
    """

    extra_space = game.cell_size / 20

    # Transversal Lines - Vertical
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 9.5),
                           (game.cell_size * y) + game.gui_size + (extra_space * 3),
                           (game.cell_size * x) + (extra_space * 10.5),
                           (game.cell_size * (y + 1)) + game.gui_size - (extra_space * 3),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Transversal Lines - Horizontal
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 3),
                           (game.cell_size * y) + game.gui_size + (extra_space * 9.5),
                           (game.cell_size * (x + 1)) - (extra_space * 3),
                           (game.cell_size * y) + game.gui_size + (extra_space * 10.5),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Major Body
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                           (game.cell_size * y) + game.gui_size + (extra_space * 7),
                           (game.cell_size * x) + (extra_space * 15),
                           (game.cell_size * y) + game.gui_size + (extra_space * 13),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Upper Details
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 6),
                           (game.cell_size * y) + game.gui_size + (extra_space * 6),
                           (game.cell_size * x) + (extra_space * 14),
                           (game.cell_size * y) + game.gui_size + (extra_space * 7),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 7),
                           (game.cell_size * y) + game.gui_size + (extra_space * 5),
                           (game.cell_size * x) + (extra_space * 13),
                           (game.cell_size * y) + game.gui_size + (extra_space * 6),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Bottom Details
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 6),
                           (game.cell_size * y) + game.gui_size + (extra_space * 13),
                           (game.cell_size * x) + (extra_space * 14),
                           (game.cell_size * y) + game.gui_size + (extra_space * 14),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 7),
                           (game.cell_size * y) + game.gui_size  + (extra_space * 14),
                           (game.cell_size * x) + (extra_space * 13),
                           (game.cell_size * y) + game.gui_size  + (extra_space * 15),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Upper-Left Particle
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                           (game.cell_size * y) + game.gui_size + (extra_space * 5),
                           (game.cell_size * x) + (extra_space * 6),
                           (game.cell_size * y) + game.gui_size + (extra_space * 6),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Upper-Right Particle
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 14),
                           (game.cell_size * y) + game.gui_size + (extra_space * 5),
                           (game.cell_size * x) + (extra_space * 15),
                           (game.cell_size * y) + game.gui_size + (extra_space * 6),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Bottom-Left Particle
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                           (game.cell_size * y) + game.gui_size + (extra_space * 14),
                           (game.cell_size * x) + (extra_space * 6),
                           (game.cell_size * y) + game.gui_size + (extra_space * 15),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Bottom-Right Particle
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 14),
                           (game.cell_size * y) + game.gui_size + (extra_space * 14),
                           (game.cell_size * x) + (extra_space * 15),
                           (game.cell_size * y) + game.gui_size + (extra_space * 15),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_1"])

    # Reflection
    gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 7),
                           (game.cell_size * y) + game.gui_size + (extra_space * 7),
                           (game.cell_size * x) + (extra_space * 9),
                           (game.cell_size * y) + game.gui_size + (extra_space * 9),
                           outline=PROFILE["MINE_OUTLINE"], fill=PROFILE["MINE_2"])

def draw_number(game: 'MinesweeperGame', x: int, y: int, number: int) -> None:
    """
    Draws a little pixel art of the number that is the value of the cell.
    """

    number_color = PROFILE[f"NUMBER_{number}"]
    extra_space = game.cell_size / 20

    if number == 1:

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 7),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13.5),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15.5),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 9),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9.5),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 14.5),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 7),
                               (game.cell_size * y) + game.gui_size + (extra_space * 8.5),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9.5),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7.5),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 8.5),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 9),
                               (game.cell_size * y) + game.gui_size + (extra_space * 6.5),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7.5),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 10),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5.5),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 6.5),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

    elif number == 2:

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 12),
                               (game.cell_size * x) + (extra_space * 9),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 6),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                               (game.cell_size * x) + (extra_space * 11),
                               (game.cell_size * y) + game.gui_size + (extra_space * 12),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 10),
                               (game.cell_size * x) + (extra_space * 13),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 10),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 10),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 11),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                               (game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 8),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 6),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 7),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 13),
                               (game.cell_size * y) + game.gui_size + (extra_space * 6),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

    elif number == 3:

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 6),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 14),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

    elif number == 4:

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 11),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 6),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                               (game.cell_size * x) + (extra_space * 9),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 7),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 10),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

    elif number == 5:

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                               (game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 10),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 14),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

    elif number == 6:

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 6),
                               (game.cell_size * x) + (extra_space * 6),
                               (game.cell_size * y) + game.gui_size + (extra_space * 14),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 6),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 10),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 14),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

    elif number == 7:

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 11),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 10),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                               (game.cell_size * x) + (extra_space * 13),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

        gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 9),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

    elif number == 8:

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 6),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 5),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 7),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 8),
                               (game.cell_size * y) + game.gui_size + (extra_space * 13),
                               (game.cell_size * x) + (extra_space * 12),
                               (game.cell_size * y) + game.gui_size + (extra_space * 15),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 6),
                               (game.cell_size * x) + (extra_space * 6),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 6),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 9),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 5),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                               (game.cell_size * x) + (extra_space * 6),
                               (game.cell_size * y) + game.gui_size + (extra_space * 14),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

       gamelib.draw_rectangle((game.cell_size * x) + (extra_space * 14),
                               (game.cell_size * y) + game.gui_size + (extra_space * 11),
                               (game.cell_size * x) + (extra_space * 15),
                               (game.cell_size * y) + game.gui_size + (extra_space * 14),
                                outline=PROFILE["NUMBER_OUTLINE"], fill=number_color)

def draw_buttons(game: 'MinesweeperGame') -> None:
    """
    Draws all the buttons of the game.
    """

    for button in game.buttons:

        gamelib.draw_rectangle(button.x1,
                               button.y1,
                               button.x2,
                               button.y2,
                               width=(game.cell_size // 15),
                               outline=PROFILE["BUTTON_OUTLINE" if button is not game.new_game else "GUI_OUTLINE_1"],
                               fill=PROFILE["BUTTON_1" if button is not game.new_game else "NEW_GAME_1"],
                               activefill=PROFILE["BUTTON_2" if button is not game.new_game else "NEW_GAME_2"])

        if button.msg:

            cx, cy = button.center()

            gamelib.draw_text(button.msg,
                            cx,
                            cy,
                            size=(game.cell_size // 2),
                            justify='c', anchor='c',
                            fill=PROFILE["BUTTON_TEXT"])

    x1, y1, x2, y2 = game.new_game.all_coord()

    gamelib.draw_rectangle(x1,
                           y1,
                           x1 + (game.width * 0.004166667),
                           y2 - (game.gui_size * 0.02),
                           outline=PROFILE["CELL_OUTLINE"], fill=PROFILE["CELL_COLOR_2"])

    gamelib.draw_rectangle(x1,
                           y1,
                           x2 - (game.width * 0.002),
                           y1 + (game.gui_size * 0.08),
                           outline=PROFILE["CELL_OUTLINE"], fill=PROFILE["CELL_COLOR_2"])

def draw_counter(game: 'MinesweeperGame', x1: int, y1: int, x2: int, y2: int) -> None:
    """
    Draws the flag counter which tells how much flags should be left
    (and, if used correctly, aldo how many mines there is still).

    It can enter in negative values. This is intentional as it tells
    that the player has placed more flags than mines there should be
    on the grid.
    """

    gamelib.draw_rectangle(0,
                           0,
                           game.width * 0.15,
                           game.gui_size,
                           outline=PROFILE["GUI_OUTLINE_1"], fill=PROFILE["GUI_3"])

    digits = str(game.flags)
    digits_amount = len(digits)

    if digits_amount > 3:

        space_per_digit = (x2 - x1) / digits_amount

    else:

        space_per_digit = (x2 - x1) / 3

        digits = [char for char in digits]

        while len(digits) < 3:

            digits.insert((1 if '-' in digits else 0), '0')

        digits = ''.join(digits)

    for d in range(len(digits)):

        draw_counter_number(x1 + (space_per_digit * d),
                            y1,
                            x1 + (space_per_digit * (d + 1)),
                            y2,
                            digits[d])
    

def draw_counter_number(x1: int, y1: int, x2: int, y2: int, n: str) -> None:
    """
    Given an area to work with, it draws a number (or a hyphen) in a
    counter.
    """

    if n not in "-0123456789":

        raise Exception(f"Parameter {n = } should be a decimal digit ('0'-'9') or a hyphen character ('-').")

    if n == '-': number = (0, 0, 0, 1, 0, 0, 0)

    elif n == '0': number = (1, 1, 1, 0, 1, 1, 1)

    elif n == '1': number = (0, 0, 1, 0, 0, 0, 1)

    elif n == '2': number = (0, 1, 1, 1, 1, 1, 0)

    elif n == '3': number = (0, 1, 1, 1, 0, 1, 1)

    elif n == '4': number = (1, 0, 1, 1, 0, 0, 1)

    elif n == '5': number = (1, 1, 0, 1, 0, 1, 1)

    elif n == '6': number = (1, 1, 0, 1, 1, 1, 1)

    elif n == '7': number = (0, 1, 1, 0, 0, 0, 1)

    elif n == '8': number = (1, 1, 1, 1, 1, 1, 1)

    elif n == '9': number = (1, 1, 1, 1, 0, 1, 1)

    extra_x, extra_y = ((x2 - x1) / 50), ((y2 - y1) / 95) # Grid is 50x95px as template

    gamelib.draw_polygon([x1 + (extra_x * 2),
                          y1 + (extra_y * 4),
                          x1 + (extra_x * 14),
                          y1 + (extra_y * 15),
                          x1 + (extra_x * 14),
                          y1 + (extra_y * 35),
                          x1 + (extra_x * 2),
                          y1 + (extra_y * 45)],
                          outline=PROFILE["COUNTER_OUTLINE"],
                          fill=PROFILE[f"COUNTER_{'1' if number[0] else '2'}"])

    gamelib.draw_polygon([x1 + (extra_x * 4),
                          y1 + (extra_y * 2),
                          x1 + (extra_x * 15),
                          y1 + (extra_y * 14),
                          x1 + (extra_x * 35),
                          y1 + (extra_y * 14),
                          x1 + (extra_x * 45),
                          y1 + (extra_y * 2)],
                          outline=PROFILE["COUNTER_OUTLINE"],
                          fill=PROFILE[f"COUNTER_{'1' if number[1] else '2'}"])

    gamelib.draw_polygon([x1 + (extra_x * 48),
                          y1 + (extra_y * 4),
                          x1 + (extra_x * 35),
                          y1 + (extra_y * 15),
                          x1 + (extra_x * 35),
                          y1 + (extra_y * 35),
                          x1 + (extra_x * 48),
                          y1 + (extra_y * 45)],
                          outline=PROFILE["COUNTER_OUTLINE"],
                          fill=PROFILE[f"COUNTER_{'1' if number[2] else '2'}"])

    gamelib.draw_polygon([x1 + (extra_x * 5),
                          y1 + (extra_y * 47),
                          x1 + (extra_x * 10),
                          y1 + (extra_y * 40),
                          x1 + (extra_x * 39),
                          y1 + (extra_y * 40),
                          x1 + (extra_x * 45),
                          y1 + (extra_y * 47),
                          x1 + (extra_x * 39),
                          y1 + (extra_y * 54),
                          x1 + (extra_x * 10),
                          y1 + (extra_y * 54)],
                          outline=PROFILE["COUNTER_OUTLINE"],
                          fill=PROFILE[f"COUNTER_{'1' if number[3] else '2'}"])

    gamelib.draw_polygon([x1 + (extra_x * 2),
                          y1 + (extra_y * 49),
                          x1 + (extra_x * 15),
                          y1 + (extra_y * 59),
                          x1 + (extra_x * 15),
                          y1 + (extra_y * 79),
                          x1 + (extra_x * 2),
                          y1 + (extra_y * 90)],
                          outline=PROFILE["COUNTER_OUTLINE"],
                          fill=PROFILE[f"COUNTER_{'1' if number[4] else '2'}"])

    gamelib.draw_polygon([x1 + (extra_x * 4),
                          y1 + (extra_y * 92),
                          x1 + (extra_x * 15),
                          y1 + (extra_y * 80),
                          x1 + (extra_x * 35),
                          y1 + (extra_y * 80),
                          x1 + (extra_x * 45),
                          y1 + (extra_y * 92)],
                          outline=PROFILE["COUNTER_OUTLINE"],
                          fill=PROFILE[f"COUNTER_{'1' if number[5] else '2'}"])

    gamelib.draw_polygon([x1 + (extra_x * 48),
                          y1 + (extra_y * 49),
                          x1 + (extra_x * 35),
                          y1 + (extra_y * 59),
                          x1 + (extra_x * 35),
                          y1 + (extra_y * 79),
                          x1 + (extra_x * 48),
                          y1 + (extra_y * 90)],
                          outline=PROFILE["COUNTER_OUTLINE"],
                          fill=PROFILE[f"COUNTER_{'1' if number[6] else '2'}"])



def draw_figure(x1: int, y1: int, x2: int, y2: int, grid_cols: int, grid_rows: int, colors_dict: dict) -> None:
    """
    ______________________________________________________________________

    x1, y1, x2, y2: <int>

    grid_cols, grid_rows: <int>

    colors_dict: <dict> --> {<tuple> : <str>, <tuple> : <str>, ... , <tuple> : <str>}
    --> {(<int>, <int>) : <str>, (<int>, <int>) : <str>, ... , (<int>, <int>) : <str>}


    ---> None
    ______________________________________________________________________

    Given an area to play with, the grid sizes into which the space is divided,
    and a dictionary with all colors to fill, this function draws any pixel art as
    it draws a color rectangle on any given coordinates inside the area and designated
    grid.
    """

    cell_x = (x2 - x1) / grid_cols
    cell_y = (y2 - y1) / grid_rows

    for x in range(grid_cols):

        for y in range(grid_rows):

            gamelib.draw_rectangle((x * cell_x) + x1,
                                   (y * cell_y) + y1,
                                   ((x + 1) * cell_x) + x1,
                                   ((y + 1) * cell_y) + y1,
                                   outline='', fill=(colors_dict.get((x, y), '')))

def draw_logo(game: 'MinesweeperGame') -> None:
    """
    Draws the NLGS logo and its variations.
    """

    cols, _ = game.dimensions()

    humor = (f"NLGS_{game.humor}" if (game.humor and f'NLGS_{game.humor}' in FIGURES) else "NLGS_NORMAL") + (f"_MUTE" if not game.has_audio else '')

    draw_figure(game.cell_size * (cols / 2) - (game.gui_size / 2),
                0,
                game.cell_size * (cols / 2) + (game.gui_size / 2),
                game.gui_size,
                26,
                26,
                (FIGURES[humor]))

def draw_screen(game: 'MinesweeperGame') -> None:
    """
    Draws the entirety of the elements on the screen.
    """

    draw_grid(game)
    draw_GUI(game)

    draw_buttons(game)

    draw_counter(game, 0, 0, game.width * 0.15, game.gui_size)

    draw_logo(game)