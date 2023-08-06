"""
This module contains all functions that belong to graphics handling
and drawing on the game screen.
"""

from .. import gamelib
from .pifiles import map_color_profiles

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from .picross import PicrossGame

SELECTED_THEME = "BORED_GREY"
"""
Can select from the following themes:

'BORED_GREY': The default one, the most 'meh'.
"""

PROFILE = map_color_profiles()[SELECTED_THEME]

NLGS_LOGO = {                                                                                                                                                            (5, 0) : PROFILE["GOLD"],          (6, 0) : PROFILE["GOLD"],          (7, 0) : PROFILE["GOLD"],
                                                                                                       (3, 1) : PROFILE["GOLD"],        (4, 1) : PROFILE["GOLD"],        (5, 1) : PROFILE["DARK_GREY_3"],   (6, 1) : PROFILE["DARK_GREY_3"],   (7, 1) : PROFILE["DARK_GREY_3"],   (8, 1) : PROFILE["GOLD"],         (9, 1) : PROFILE["GOLD"],
                                                                       (2, 2) : PROFILE["GOLD"],       (3, 2) : PROFILE["BLACK"],       (4, 2) : PROFILE["BLACK"],       (5, 2) : PROFILE["BLACK"],         (6, 2) : PROFILE["BLACK"],         (7, 2) : PROFILE["DARK_GREY_3"],   (8, 2) : PROFILE["DARK_GREY_3"],  (9, 2) : PROFILE["DARK_GREY_3"],  (10, 2) : PROFILE["GOLD"],
                                       (1, 3) : PROFILE["GOLD"],       (2, 3) : PROFILE["BLACK"],      (3, 3) : PROFILE["BLACK"],       (4, 3) : PROFILE["BLACK"],       (5, 3) : PROFILE["BLACK"],         (6, 3) : PROFILE["BLACK"],         (7, 3) : PROFILE["BLACK"],         (8, 3) : PROFILE["BLACK"],        (9, 3) : PROFILE["DARK_GREY_3"],  (10, 3) : PROFILE["DARK_GREY_3"], (11, 3) : PROFILE["GOLD"],
                                       (1, 4) : PROFILE["GOLD"],       (2, 4) : PROFILE["BLACK"],      (3, 4) : PROFILE["SKIN_COLOR"],  (4, 4) : PROFILE["SKIN_COLOR"],  (5, 4) : PROFILE["SKIN_COLOR"],    (6, 4) : PROFILE["BLACK"],         (7, 4) : PROFILE["SKIN_COLOR"],    (8, 4) : PROFILE["DARK_GREY_3"],  (9, 4) : PROFILE["BLACK"],        (10, 4) : PROFILE["DARK_GREY_3"], (11, 4) : PROFILE["GOLD"],
             (0, 5) : PROFILE["GOLD"], (1, 5) : PROFILE["BLACK"],      (2, 5) : PROFILE["SKIN_COLOR"], (3, 5) : PROFILE["SKIN_COLOR"],  (4, 5) : PROFILE["SKIN_COLOR"],  (5, 5) : PROFILE["BLACK"],         (6, 5) : PROFILE["SKIN_COLOR"],    (7, 5) : PROFILE["SKIN_COLOR"],    (8, 5) : PROFILE["DARK_GREY_3"],  (9, 5) : PROFILE["DARK_GREY_3"],  (10, 5) : PROFILE["DARK_GREY_3"], (11, 5) : PROFILE["DARK_GREY_3"], (12, 5) : PROFILE["GOLD"],
             (0, 6) : PROFILE["GOLD"], (1, 6) : PROFILE["SKIN_COLOR"], (2, 6) : PROFILE["SKIN_COLOR"], (3, 6) : PROFILE["SKIN_COLOR"],  (4, 6) : PROFILE["DARK_BROWN"],  (5, 6) : PROFILE["SKIN_COLOR"],    (6, 6) : PROFILE["DARK_BROWN"],    (7, 6) : PROFILE["SKIN_COLOR"],    (8, 6) : PROFILE["DARK_GREY_3"],  (9, 6) : PROFILE["DARK_GREY_3"],  (10, 6) : PROFILE["DARK_GREY_3"], (11, 6) : PROFILE["DARK_GREY_3"], (12, 6) : PROFILE["GOLD"],
             (0, 7) : PROFILE["GOLD"], (1, 7) : PROFILE["SKIN_COLOR"], (2, 7) : PROFILE["SKIN_COLOR"], (3, 7) : PROFILE["SKIN_COLOR"],  (4, 7) : PROFILE["DARK_BROWN"],  (5, 7) : PROFILE["SKIN_COLOR"],    (6, 7) : PROFILE["DARK_BROWN"],    (7, 7) : PROFILE["SKIN_COLOR"],    (8, 7) : PROFILE["DARK_GREY_3"],  (9, 7) : PROFILE["DARK_GREY_3"],  (10, 7) : PROFILE["DARK_GREY_3"], (11, 7) : PROFILE["DARK_GREY_3"], (12, 7) : PROFILE["GOLD"],
                                       (1, 8) : PROFILE["GOLD"],       (2, 8) : PROFILE["SKIN_COLOR"], (3, 8) : PROFILE["SKIN_COLOR"],  (4, 8) : PROFILE["SKIN_COLOR"],  (5, 8) : PROFILE["SKIN_COLOR"],    (6, 8) : PROFILE["SKIN_COLOR"],    (7, 8) : PROFILE["SKIN_COLOR"],    (8, 8) : PROFILE["DARK_GREY_3"],  (9, 8) : PROFILE["DARK_GREY_3"],  (10, 8) : PROFILE["DARK_GREY_3"], (11, 8) : PROFILE["GOLD"],
                                       (1, 9) : PROFILE["GOLD"],       (2, 9) : PROFILE["SKIN_COLOR"], (3, 9) : PROFILE["SKIN_COLOR"],  (4, 9) : PROFILE["CANDY_RED"],   (5, 9) : PROFILE["CANDY_RED"],     (6, 9) : PROFILE["SKIN_COLOR"],    (7, 9) : PROFILE["SKIN_COLOR"],    (8, 9) : PROFILE["DARK_GREY_3"],  (9, 9) : PROFILE["DARK_GREY_3"],  (10, 9) : PROFILE["DARK_GREY_3"], (11, 9) : PROFILE["GOLD"],
                                                                       (2, 10) : PROFILE["GOLD"],      (3, 10) : PROFILE["SKIN_COLOR"], (4, 10) : PROFILE["SKIN_COLOR"], (5, 10) : PROFILE["SKIN_COLOR"],   (6, 10) : PROFILE["SKIN_COLOR"],   (7, 10) : PROFILE["SKIN_COLOR"],   (8, 10) : PROFILE["DARK_GREY_3"], (9, 10) : PROFILE["DARK_GREY_3"], (10, 10) : PROFILE["GOLD"],
                                                                                                       (3, 11) : PROFILE["GOLD"],       (4, 11) : PROFILE["GOLD"],       (5, 11) : PROFILE["SKIN_COLOR"],   (6, 11) : PROFILE["DARK_GREY_3"],  (7, 11) : PROFILE["DARK_GREY_3"],  (8, 11) : PROFILE["GOLD"],        (9, 11) : PROFILE["GOLD"],
                                                                                                                                                                         (5, 12) : PROFILE["GOLD"],         (6, 12) : PROFILE["GOLD"],         (7, 12) : PROFILE["GOLD"]
            }
"""
The legendary NLGS logo.
"""

def draw_GUI(game: 'PicrossGame') -> None:
    """
    Draws the Graphic User Interface of the game.

    It includes some info texts, and the counters used to display some game attributes.
    """

    gamelib.draw_rectangle(0, 0, game.width + 10, game.gui_size, outline=PROFILE["DARK_GREY_2"], fill=PROFILE["DARK_GREY_1"])

    gamelib.draw_text(f"Current Mistakes: {game.mistakes_count} / {game.max_mistakes}", (game.width / 50), (game.width / 25), size=(game.width // 33), anchor='w', fill=PROFILE["WHITE"])

    actual_grid_x, actual_grid_y = game.dimensions()

    if (not game.grid_x == (actual_grid_x - 1)) or (not game.grid_y == (actual_grid_y - 1)): # The actual size also counts the indexes

        gamelib.draw_text(f"Selected values differ!\nPress '{game.new_game.msg}'\n <= to apply",
                          110, 35, size=(game.width // 50), justify="left", anchor="nw", fill=PROFILE["WHITE"])

    gamelib.draw_text("Grid Dimensions:", (game.width * 0.69), (game.width / 25), size=(game.width // 33), anchor='c', fill=PROFILE["WHITE"])

    cols_x, cols_y = (game.width * 0.65), (game.gui_size * 0.65)
    rows_x, rows_y = (game.width * 0.73), (game.gui_size * 0.65)

    gamelib.draw_text("Cols (x)", (game.width * 0.51), cols_y, size=(game.width // 33), anchor='c', fill=PROFILE["WHITE"])
    gamelib.draw_text("Rows (y)", (game.width * 0.88), rows_y, size=(game.width // 33), anchor='c', fill=PROFILE["WHITE"])

    frame_margin = int(game.gui_size / 6.666)

    gamelib.draw_rectangle(cols_x - frame_margin, cols_y - frame_margin, cols_x + frame_margin, cols_y + frame_margin, width=(game.width // 200), outline=PROFILE["DARK_GREY_2"], fill=PROFILE["DARK_GREY_3"])
    gamelib.draw_rectangle(rows_x - frame_margin, rows_y - frame_margin, rows_x + frame_margin, rows_y + frame_margin, width=(game.width // 200), outline=PROFILE["DARK_GREY_2"], fill=PROFILE["DARK_GREY_3"])

    gamelib.draw_text(f"{game.grid_x}", cols_x, cols_y, size=(game.width // 50), anchor='c', fill=PROFILE["WHITE"])
    gamelib.draw_text(f"{game.grid_y}", rows_x, rows_y, size=(game.width // 50), anchor='c', fill=PROFILE["WHITE"])

def draw_buttons(game: 'PicrossGame'):
    """
    Draws all the buttons of the games, in their respective coordinates.
    """

    for button in game.buttons_list:

        gamelib.draw_rectangle(button.x1, button.y1, button.x2, button.y2, width=(game.width // 250), outline=PROFILE["DARK_GREY_5"], fill=PROFILE["DARK_GREY_4"], activefill=(PROFILE["GREY_2"] if button.msg else ''))

        center_x, center_y = button.center()
        if button.msg: gamelib.draw_text(button.msg, center_x, center_y, size=(game.width // 50), justify='c', anchor='c', fill=PROFILE["WHITE"])

def draw_megaphone(game: 'PicrossGame') -> None:
    """
    Draws a megaphone that shows if the game has audio or not.
    """

    if game.has_audio:

        gamelib.draw_arc((game.width * 0.91),    # x1
                         (game.gui_size * 0.05), # y1
                         (game.width * 0.98),    # x2
                         (game.gui_size * 0.35), # y2
                         start="135", outline='', fill=PROFILE["WHITE"])

        gamelib.draw_arc((game.width * 0.916),   # x1
                         (game.gui_size * 0.05), # y1
                         (game.width * 0.986),   # x2
                         (game.gui_size * 0.35), # y2
                         start="135", outline='', fill=PROFILE["DARK_GREY_4"])

        gamelib.draw_arc((game.width * 0.924),   # x1
                         (game.gui_size * 0.08), # y1
                         (game.width * 0.972),   # x2
                         (game.gui_size * 0.32), # y2
                         start="135", outline='', fill=PROFILE["WHITE"])

        gamelib.draw_arc((game.width * 0.93),    # x1
                         (game.gui_size * 0.05), # y1
                         (game.width * 0.98),    # x2
                         (game.gui_size * 0.35), # y2
                         start="135", outline='', fill=PROFILE["DARK_GREY_4"])

    else:

        gamelib.draw_line((game.width * 0.91),    # x1
                          (game.gui_size * 0.15), # y1
                          (game.width * 0.93),    # x2
                          (game.gui_size * 0.25), # y2
                          width=(game.gui_size // 50), fill=PROFILE["WHITE"])

        gamelib.draw_line((game.width * 0.93),    # x1
                          (game.gui_size * 0.15), # y1
                          (game.width * 0.91),    # x2
                          (game.gui_size * 0.25), # y2
                          width=(game.gui_size // 50), fill=PROFILE["WHITE"])

        gamelib.draw_line((game.width * 0.97),    # x1
                          (game.gui_size * 0.05), # y1
                          (game.width * 0.93),    # x2
                          (game.gui_size * 0.35), # y2
                          width=int(game.gui_size * 0.03))

    gamelib.draw_polygon([(game.width * 0.944),   # x1
                         (game.gui_size * 0.07),  # y1
                         (game.width * 0.944),    # x2
                         (game.gui_size * 0.33),  # y2
                         (game.width * 0.98),     # x3
                         (game.gui_size * 0.20)], # y3
                         outline='', fill=PROFILE["WHITE"])

    gamelib.draw_rectangle((game.width * 0.97),    # x1
                           (game.gui_size * 0.15), # y1
                           (game.width * 0.986),   # x2
                           (game.gui_size * 0.25), # y2
                           outline=PROFILE["DARK_GREY_2"], fill=PROFILE["WHITE"])

def draw_grid(game: 'PicrossGame') -> None:
    """
    Draws the grid of the game, according to the window sizes and grid columns
    and rows.
    """

    cols, rows = game.dimensions()

    index_x, index_y = game.calculate_indexes()

    cell_x = (game.width - index_x) / (cols - 1)
    cell_y = (game.height - index_y - game.gui_size) / (rows - 1)

    error_x = cell_x / 4
    error_y = cell_y / 4

    gamelib.draw_rectangle(0, game.gui_size, game.width + 10, game.height + 10, outline='', fill=PROFILE["GREY_1"])

    for j in range(1, rows):

        for i in range(1, cols):

            cell = game.grid[j][i]

            cell_color = (PROFILE["LIGHT_GREY_2"] if cell[1] else (PROFILE["BLACK"] if cell[0] else PROFILE["WHITE"]))

            gamelib.draw_rectangle(((i - 1) * cell_x) + index_x,
                                ((j - 1) * cell_y) + game.gui_size + index_y,
                                (i * cell_x) + index_x,
                                (j * cell_y) + game.gui_size + index_y,
                                outline='', fill=cell_color, activefill=(PROFILE["LIGHT_GREY_1"] if cell[1] else ''))

            if (i, j) in game.mistakes_coord:

                gamelib.draw_line(((i - 1) * cell_x) + index_x + error_x,
                                ((j - 1) * cell_y) + game.gui_size + index_y + error_y,
                                (i * cell_x) + index_x - error_x,
                                (j * cell_y) + game.gui_size + index_y - error_y,
                                width=(game.width // 150), fill=PROFILE["RED"])

                gamelib.draw_line((i * cell_x) + index_x - error_x,
                                ((j - 1) * cell_y) + game.gui_size + index_y + error_y,
                                ((i - 1) * cell_x) + index_x + error_x,
                                (j * cell_y) + game.gui_size + index_y - error_y,
                                width=(game.width // 150), fill=PROFILE["RED"])

    for x in range(cols + 1):

        gamelib.draw_line((x * cell_x) + index_x, game.gui_size, (x * cell_x) + index_x, game.height, width=(game.width // 500), fill=PROFILE["ALMOST_BLACK"])

    for y in range(rows + 1):

        gamelib.draw_line(0, (y * cell_y) + game.gui_size + index_y, game.width, (y * cell_y) + game.gui_size + index_y, width=(game.height // 700), fill=PROFILE["ALMOST_BLACK"])

def draw_index_numbers(game: 'PicrossGame') -> None:
    """
    Writes in the screen the numbers used for the indexes of the game grid.
    """

    cols, rows = game.dimensions()

    index_x, index_y = game.calculate_indexes()

    cell_x = (game.width - index_x) / (cols - 1)
    cell_y = (game.height - index_y - game.gui_size) / (rows - 1)

    for j in range(1, rows):

        row_text = "  ".join([str(number) for number in game.grid[j][0]])
        row_text_size = int(index_x //  ((game.width / 200) * len(game.grid[j][0]) + 1))

        gamelib.draw_text(row_text,
                         (index_x / 2),
                         (j * cell_y) - (cell_y / 2) + game.gui_size + index_y,
                         size=row_text_size, justify='c', anchor='c', fill=PROFILE["WHITE"])

    for i in range(1, cols):

        col_text = "\n\n".join([str(number) for number in game.grid[0][i]])
        col_text_size = int(index_y // ((game.gui_size / 33.333) * len(game.grid[0][i]) + 1))

        gamelib.draw_text(col_text,
                         (i * cell_x) - (cell_x / 2) + index_x,
                         ((index_y / 2) + game.gui_size),
                         size=col_text_size, justify='c', anchor='c', fill=PROFILE["WHITE"])

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

def draw_screen(game: 'PicrossGame') -> None:
    """
    Draws the entirety of the game elements on the screen.
    """

    draw_grid(game)
    draw_GUI(game)
    draw_buttons(game)

    draw_megaphone(game)

    draw_index_numbers(game)

    index_x, index_y = game.calculate_indexes()
    draw_figure(0, game.gui_size, index_x, index_y + game.gui_size, 13, 13, NLGS_LOGO)