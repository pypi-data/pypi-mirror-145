"""
This is a simplified Minesweeper Game, by Franco 'NLGS' Lighterman.

'Gamelib' by Diego Essaya.

More at the GitHub Repository: https://github.com/NLGS2907/gamelib-games/tree/master/minesweeper
"""

"""
This module holds the game object and all of its logic.
"""

from random import randint
from ..menu import Button
from typing import Union
from .. import gamelib
from . import graphics

__version__ = "1.0.0"

SIZE_CONSTANT = 30

MINE = 'X'

INSTRUCTIONS = """\t-=-=\tINSTRUCTIONS\t=-=-


How To Play:

    Your job is to uncover each cell of the grid without
    stepping on a mine. If that happens, you loose the
    game, as you only have one life.

    Each cell that is not a mine has a number assigned
    to it. This number indicates the numbers of mines
    that are adjacent to this cell, either vertically,
    horizontally, or diagonally. Use this information
    to your advantage.

    With a bit of logic (and some guessing) you will
    surely persevere. Good Luck!

Grid:

    * [Left Click] to reveal a cell.

    * [Right Click] to cycle through unmarked, flag, or 'dunno'.

    * [Middle Click] to reveal al adjacent cells,
      if neighbours are flagged enough.

GUI:

    * [Left Click] on 'NLGS Logo' to start new game.

    * [Right Click] on 'NLGS Logo' to exit the game.

    * [Middle Click] on 'NLGS Logo' to mute or unmute
      the game

    Click the buttons of 'Mines', 'X' and 'Y' to select
    the parameters of the new game.

    - 'X' is the number of COLUMNS of the new grid.

    - 'Y' is the number of ROWS of the new grid.

    - 'Mines' is the amount of mines to be used in the
      new grid.
      If it is set to 'Auto' it will automatically use 20% of
      the new grid.
"""

def is_in_bounds(x: int, y: int, max_x: int, max_y: int) -> bool:
    """
    Given the max values for the width and height of an area (minimum value is
    always 0 for both), it calculates if the coordinates '(x, y)' are within
    said area.
    """

    return (0 <= x <= max_x) and (0 <= y <= max_y)

class MinesweeperCell:
    """
    Tiny class for a cell representation.
    """

    def __init__(self, value: Union[str, int]) -> None:
        """
        Initializes an instance of type 'MinesweeperCell'.
        """

        self._is_hidden = True
        self.value = value
        """
        The value of MINE, or a value between 0 and 8 inclusive.

        Can also be an empty string, to indicate that an empty cell already has been visited.
        """
        self.state = 0
        """
        '0' for an unmarked cell.

        '1' for a flagged cell.

        '2' for a cell with the symbol '?'.

        All the states can cycle over.
        """
    
    @property
    def is_hidden(self) -> bool:
        """
        Defines the property 'is_hidden' of the cell.
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, new_value: bool) -> None:
        """
        Changes the value of 'self.is_hidden' so the cell is now uncovered.

        One cell should never be covered again. As such, no value other than
        'False' is accepted.
        """

        if new_value == False:

            self._is_hidden = new_value

    def cycle_state(self) -> None:
        """
        Cycles through the possible stages of a cell, if it is uncovered.
        """
        
        if self.is_hidden:

            self.state = (self.state + 1) % 3

class MinesweeperGame:
    """
    Class for holding variables of a Minesweeper game.
    """

    def __init__(self, size_constant: int, grid_cols: int=20, grid_rows: int=20, mines: int=0) -> None:
        """
        Initializes an instance of type 'MinesweeperGame'.

        'size_constant' is the size of each cell (individual width
        and heght are the same).

        'grid_cols' means the columns of the game grid.

        'grid_rows' means the rows of the game grid.

        'mines' is the amount of mines in the game grid.
        """

        if grid_cols < 10 or grid_rows < 10:

            raise Exception(f"Invalid grid dimensions: Size given is ({grid_cols}, {grid_rows}). Minimum accepted is (10, 10)")

        if mines and mines > (grid_cols * grid_rows):

            mines = grid_cols * grid_rows

        # Sizes
        self.grid_x, self.grid_y = grid_cols, grid_rows

        self.cell_size = size_constant

        self.width = self.cell_size * self.grid_x
        self.gui_size = self.width // 12
        self.height = (self.cell_size * self.grid_y) + self.gui_size

        self.mines = mines
        mines_to_use = (mines if mines > 0 else int(self.grid_x * self.grid_y * 0.2)) # If mines is note specified, use 20% of the grid.
        self.flags = mines_to_use

        self.grid = self.generate_grid(self.grid_x, self.grid_y, mines_to_use)

        # When the player loses, this cell will be highlighted
        self.loser_cell = None

        # Buttons
        self.buttons = self.generate_buttons()

        # NLGS Humor
        self.humor = "NORMAL"

        # Control Booleans
        self.has_audio = True
        self.end = False
        self.exit = False

    def dimensions(self) -> tuple[int, int]:
        """
        Returns the dimensions of the game grid.
        """

        return len(self.grid[0]), len(self.grid)

    def generate_grid(self, how_many_columns: int, how_many_rows: int, how_many_mines: int) -> list:
        """
        Generates the game grid.
        """

        grid = list()
        mines_set = set()

        while len(mines_set) < how_many_mines:

            x, y = randint(0, (how_many_columns - 1)), randint(0, (how_many_rows - 1))

            mines_set.add((x, y))

        for row in range(how_many_rows):

            row_list = list()

            for col in range(how_many_columns):
                
                if (col, row) in mines_set:

                   row_list.append(MinesweeperCell(MINE))
                   mines_set.remove((col, row)) # Don't need it anymore

                else:

                    row_list.append(MinesweeperCell(0)) # This generates [0, 0], but the first 0 is not the same as HIDDEN 

            grid.append(row_list)

        return self.generate_numbers(grid)

    def generate_numbers(self, grid: list) -> list:
        """
        Generate the numbers which tell how many mines is around them.
        """

        cols, rows = len(grid[0]), len(grid)

        for y in range(rows):

            for x in range(cols):

                if grid[y][x].value == MINE: # Ignore if it is a mine

                    continue

                count = 0

                for dx in range(-1, 2):

                    for dy in range(-1, 2):

                        if is_in_bounds((x + dx), (y + dy), (cols - 1), (rows - 1)) and grid[y + dy][x + dx].value == MINE:

                            count += 1

                grid[y][x].value = count

        return grid

    def generate_buttons(self) -> list:
        """
        ______________________________________________________________________

        ---> <list> --> [<Button>, <Button>, ... , <Button>]
        ______________________________________________________________________

        Generates the buttons of the game.
        """

        buttons_list = list()
        self.new_game = Button(self.width * 0.450333333,
                               0,
                               self.width * 0.549666666,
                               self.gui_size)

        buttons_list.append(self.new_game)

        self.cols_dn = Button(self.width * 0.6,
                              0,
                              self.width * 0.65,
                              self.gui_size,
                              '<')

        buttons_list.append(self.cols_dn)

        self.cols_up = Button(self.width * 0.75,
                              0,
                              self.width * 0.8,
                              self.gui_size,
                              '>')

        buttons_list.append(self.cols_up)

        self.rows_dn = Button(self.width * 0.8,
                              0,
                              self.width * 0.85,
                              self.gui_size,
                              '<')

        buttons_list.append(self.rows_dn)

        self.rows_up = Button(self.width * 0.95,
                              0,
                              self.width,
                              self.gui_size,
                              '>')

        buttons_list.append(self.rows_up)

        self.mines_dn = Button(self.width * 0.2,
                              0,
                              self.width * 0.25,
                              self.gui_size,
                              '<')

        buttons_list.append(self.mines_dn)

        self.mines_up = Button(self.width * 0.35,
                              0,
                              self.width * 0.4,
                              self.gui_size,
                              '>')

        buttons_list.append(self.mines_up)

        self.info = Button(self.width * 0.15,
                              0,
                              self.width * 0.2,
                              self.gui_size,
                              'i')

        buttons_list.append(self.info)

        return buttons_list

    def search_coords(self, x: int, y: int) -> tuple[int, int]:
        """
        Given the (x, y) coordinates (in pixels) of a click, it
        searches to which cell of the grid it corresponds to.
        """

        cell_x = x // self.cell_size
        cell_y = (y - self.gui_size) // self.cell_size

        return cell_x, cell_y

    def reveal_mines(self) -> None:
        """
        Uncovers all the cells that contain a main.

        This function is meant to be called once and only once
        the game ended.
        """

        cols, rows = self.dimensions()

        for x in range(cols):

            for y in range(rows):

                cell = self.grid[y][x]

                if cell.value == MINE and not cell.state == 1: # Is a mine and is not flagged

                    cell.is_hidden = False

    def reveal_cells(self, x: int, y: int) -> None:
        """
        Uncovers the content of a cell and also of its neighbours,
        if the value is 0.
        """

        cell = self.grid[y][x]
        cell.is_hidden = False

        cols, rows = self.dimensions()

        for dx in range(-1, 2):

            for dy in range(-1, 2):

                if is_in_bounds((x + dx), (y + dy), (cols - 1), (rows - 1)):

                    neighbour = self.grid[y + dy][x + dx]
                    if neighbour.state == 0: neighbour.is_hidden = False

                    if neighbour.value == 0 and neighbour.state == 0:

                        neighbour.value = ''
                        self.reveal_cells(x + dx, y + dy)


    def process_click(self, x: int, y: int, click_type: int) -> None:
        """
        Given the coordinates and the type of the click, it processes
        the click action into its corresponding actions.

        Returns a boolean that says if an action was performed with
        such click.
        """

        if 0 <= x <= self.width and self.gui_size < y <= self.height and not self.end:

            cell_x, cell_y = self.search_coords(x, y)

            cell = self.grid[cell_y][cell_x]

            if not cell.is_hidden: # Cell was clicked already.

                if click_type == 2: # Is midddle click.

                    flag_count = 0

                    for dx in range(-1, 2):

                        for dy in range(-1, 2):

                            cols, rows = self.dimensions()

                            if is_in_bounds((cell_x + dx), (cell_y + dy), (cols - 1), (rows - 1)):

                                neighbour = self.grid[cell_y + dy][cell_x + dx]

                                if neighbour.state == 1: # If it is flagged.

                                    flag_count += 1

                    if flag_count >= (cell.value if not cell.value == '' else 0):

                        for dx in range(-1, 2):

                            for dy in range(-1, 2):

                                if is_in_bounds((cell_x + dx), (cell_y + dy), (cols - 1), (rows - 1)):

                                    neighbour = self.grid[cell_y + dy][cell_x + dx]

                                    if neighbour.state == 0:
                                        
                                        neighbour.is_hidden = False

                                        if neighbour.value == MINE:

                                            self.loser_cell = neighbour
                                            self.reveal_mines()

                                        elif neighbour.value == 0:

                                            self.reveal_cells((cell_x + dx), (cell_y + dy))

            if click_type == 3: # Is secondary click.

                cell.cycle_state()

                if cell.state == 1: # Is flagged

                    self.flags -= 1

                elif cell.state == 2:

                    self.flags += 1

                if cell.is_hidden and self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/marked.wav")

            elif click_type == 1 and cell.state == 0: # Is primary click and cell is unmarked.

                if cell.value == MINE:

                    self.loser_cell = cell
                    self.reveal_mines()

                elif cell.value == 0:

                    self.reveal_cells(cell_x, cell_y)

                if cell.is_hidden and self.has_audio:
                    
                    gamelib.play_sound(f"gamelibgames/minesweeper/sfx/uncovered_{cell.value}.wav")

                cell.is_hidden = False

        else:

            for button in self.buttons:

                if button.is_inside(x, y):

                    if button is self.new_game:

                        if click_type == 1:

                            self.init_new_game(self.grid_x, self.grid_y, self.mines)

                        elif click_type == 2:

                            self.has_audio = not self.has_audio

                        elif click_type == 3:

                            self.exit = True

                    elif button is self.cols_up:

                        self.grid_x += 1

                        if self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/button_up.wav")

                    elif button is self.cols_dn:

                        if self.grid_x > 10:

                            self.grid_x -= 1

                        if self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/button_dn.wav")

                    elif button is self.rows_up:

                        self.grid_y += 1

                        if self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/button_up.wav")

                    elif button is self.rows_dn:

                        if self.grid_y > 10:

                            self.grid_y -= 1

                        if self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/button_dn.wav")

                    elif button is self.mines_up:

                        cols, rows = self.dimensions()

                        if self.mines <= 0:

                            self.mines = 1

                        elif self.mines < (cols * rows): self.mines += 1

                        if self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/button_up.wav")

                    elif button is self.mines_dn:

                        if self.mines and self.mines > 0:

                            self.mines -= 1

                        if self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/button_dn.wav")

                    elif button is self.info:

                        if self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/popup.wav")

                        gamelib.say(INSTRUCTIONS)

    def did_it_end(self) -> tuple[bool, bool]:
        """
        Returns a tuple in which the first element indicates if the
        game ended already. The second one indicates if it was a
        victory or not.
        """

        if self.loser_cell: # Landed on a mine

            if not self.end and self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/boom.wav")

            self.humor = "DEAD"
            return True, False

        cols, rows = self.dimensions()

        for x in range(cols):

            for y in range(rows):

                cell = self.grid[y][x]

                if cell.value == MINE and cell.state == 1:

                    continue

                if cell.is_hidden:

                    return False, False

        self.humor = "HAPPY"
        if not self.end and self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/victory.wav")
        return True, True

    def init_new_game(self, grid_x: int, grid_y: int, mines: int) -> None:
        """
        Begins a new game with the current values for the
        columns and rows of the game grid, and also the amount
        of mines.
        """

        self.end = False
        self.loser_cell = None

        mines_to_use = (mines if mines > 0 else int(self.grid_x * self.grid_y * 0.2))
        self.flags = mines_to_use

        self.width = self.cell_size * grid_x
        self.gui_size = self.width // 12
        self.height = (self.cell_size * grid_y) + self.gui_size

        self.humor = "NORMAL"
        self.grid = self.generate_grid(grid_x, grid_y, mines_to_use)
        self.buttons = self.generate_buttons()

        gamelib.resize(self.width, self.height)

        if self.has_audio: gamelib.play_sound("gamelibgames/minesweeper/sfx/new_game.wav")


def main() -> None:
    """
    Main function. Shouldn't be called more than once.
    """

    game = MinesweeperGame(SIZE_CONSTANT, 20, 20)

    gamelib.title("Plain Minesweeper! by NLGS")
    gamelib.resize(game.width, game.height)
    gamelib.icon("gamelibgames/minesweeper/img/icon/minesweeper_logo.gif")

    while gamelib.loop(fps=60):

        if game.exit:
            break

        gamelib.draw_begin()
        graphics.draw_screen(game)
        gamelib.draw_end()

        click = gamelib.wait(gamelib.EventType.ButtonPress)

        if click: game.process_click(click.x, click.y, click.mouse_button)

        ended, _ = game.did_it_end()

        if ended:
            game.end = True


if __name__ == "__main__":
    gamelib.init(main)