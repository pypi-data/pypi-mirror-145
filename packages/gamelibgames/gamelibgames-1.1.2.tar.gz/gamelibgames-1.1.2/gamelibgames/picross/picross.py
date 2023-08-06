"""
This is a simplified Picross Game, by Franco 'NLGS' Lighterman.

'Gamelib' by Diego Essaya.

More at the GitHub Repository: https://github.com/NLGS2907/gamelib-games/tree/master/picross
"""

"""
This module contains the Game Object and all functions and methods that
belong to logic processing.
"""

from .. import gamelib
from ..menu import Button
from . import graphics

from random import choice
from typing import Union, Callable

__version__ = "1.1.0"

WIDTH = 500
HEIGHT = 700

def column_list(grid: list, x: int, with_index: bool=True) -> list:
    """
    ______________________________________________________________________

    grid: <list> --> [None, <list>*, <list>*, ... , <list>*]

            *<list> --> [[<list>, <int>, <int>, ... , <int>],
                        [<list>, <int>, <int>, ... , <int>]
                        [<list>, <int>, <int>, ... , <int>]]

    x: <int>

    with_index: <bool>


    ---> <list> --> [<list>*, <int>, <int>, ... , <int>]

        *<list> --> [<int>, <int>, ... , <int>]
    ______________________________________________________________________

    Returns a list with the values of a selected column of a given grid 'grid'.

    'x' must be a valid value between 0 and the number of columns of the grid.

    'with_index' indicates if the returned list includes the index of said column.
    """

    cols, rows = len(grid[0]), len(grid)

    if x < 0 or x >= cols:

        raise Exception(f"Column {x} is out of range")

    temp_list = list()

    for i in range((0 if with_index else 1), rows):

        temp_list.append(grid[i][x])
    
    return temp_list

def row_list(grid: list, y: int, with_index: bool=True) -> list:
    """
    ______________________________________________________________________

    grid: <list> --> [None, <list>*, <list>*, ... , <list>*]

            *<list> --> [[<list>, <int>, <int>, ... , <int>],
                        [<list>, <int>, <int>, ... , <int>]
                        [<list>, <int>, <int>, ... , <int>]]

    y: <int>

    with_index: <bool>


    ---> <list> --> [<list>*, <int>, <int>, ... , <int>]

        *<list> --> [<int>, <int>, ... , <int>]
    ______________________________________________________________________

    Returns a list with the values of a selected row of a given grid 'grid'.

    'y' must be a valid value between 0 and the number of rows of the grid.

    'with_index' indicates if the returned list includes the index of said row.
    """

    cols, rows = len(grid[0]), len(grid)

    if y < 0 or y >= rows:

        raise Exception(f"Row {y} is out of range")

    temp_list = list()

    for j in range((0 if with_index else 1), cols):

        temp_list.append(grid[y][j])
    
    return temp_list

def split_filter(list_to_filter: list, filter_function: Union[Callable, None]=None) -> list:
    """
    Given a list and a filter function, it returns another list of sublists
    which each have the elements of 'list_to_filter' to which the filter function
    'filter_function' returns 'True', using those the 'filter_function' returns
    'False' from as a separator.

    example: converts from [2, 4, 5, 6, 7, 8, 10, 12] to [[2, 4], [6], [8, 10, 12]],
    should the filter function be, say, 'lambda x: x % 2 == 0' (the element is even)

    If the filter function is None, then evaluates if the elements themselves are True
    or False.
    """
    big_list = list()
    sublist = list()

    can_add = False

    for element in list_to_filter:

        if (filter_function(element) if filter_function else element):

            if element is list_to_filter[len(list_to_filter) - 1]:

                can_add = True

            sublist.append(element)
        
        else:

            can_add = True

        if can_add:

            can_add = False

            if sublist:

                big_list.append(sublist)
                sublist = list()

    return big_list

class PicrossGame:
    """
    Main class with the purpose of storing all the games variables.
    """

    def __init__(self, initial_width: int, initial_height: int, grid_cols: int=10, grid_rows: int=10, how_many_mistakes: int=3, must_discover_grid: bool=False) -> None:
        """
        Initalizes an instance of type 'PicrossGame'.

        'initial_width' and 'initial_height' are the sizes of the game window.

        'grid_cols' and 'grid_rows' are the dimensions of the game grid. The minum allowed
        is '4' for both values.

        'how_many_mistakes' is the max number of mistakes the player is allowed
        to do before the game is considered lost.

        'must_discover_grid' is an option which indicates if the games ends when the
        player discovers all marked tiles, or when they reveal all the grid, regardless
        of the cell is marked or not. It is 'False' by default.
        """

        if initial_width > initial_height:

            print(f"[WARNING]: Height should always be greater than Width...\nReversing the values from ({initial_width}, {initial_height}) tp ({initial_height}, {initial_width})")

            initial_width, initial_height = initial_height, initial_width

        if grid_cols < 4 or grid_rows < 4:

            raise Exception(f"Invalid grid dimensions: Size given is ({grid_cols}, {grid_rows}). Minimum accepted is (4, 4)")

        # Dimensions
        self.width, self.height = initial_width, initial_height

        # Even though there is a function that returns the dimensions, these can change with time,
        # and differ from the actual grid dimensions values.
        self.grid_x, self.grid_y = grid_cols, grid_rows

        self.gui_size = self.height // 7

        # Buttons
        self.buttons_list = list()
        self.generate_buttons()

        # Grid
        self.grid = self.generate_level(self.grid_x, self. grid_y)

        # Mistakes Control
        self.max_mistakes = how_many_mistakes
        self.mistakes_count = 0
        self.mistakes_coord = list()

        # Control booleans
        self.ended = False
        self.has_audio = True
        self.has_to_clear_grid = must_discover_grid

    def generate_buttons(self) -> None:
        """
        Generates the buttons that are meant to be used in the game.
        """

        cols_x, cols_y = (self.width * 0.65), (self.gui_size * 0.65)
        rows_x, rows_y = (self.width * 0.73), (self.gui_size * 0.65)

        frame_margin = int(self.gui_size / 6.666)

        self.new_game = Button((self.width / 50), (self.width / 10), (self.width / 5), (self.gui_size * 0.9), "New Game")
        self.buttons_list.append(self.new_game)

        self.cols_up = Button(cols_x - frame_margin,
                              cols_y - (2 * frame_margin),
                              cols_x + frame_margin,
                              cols_y - frame_margin,
                              "/\\")
        self.buttons_list.append(self.cols_up)

        self.cols_dn = Button(cols_x - frame_margin,
                              cols_y + frame_margin,
                              cols_x + frame_margin,
                              cols_y +  (2 * frame_margin),
                              "\/")
        self.buttons_list.append(self.cols_dn)

        self.rows_up = Button(rows_x - frame_margin,
                              rows_y - (2 * frame_margin),
                              rows_x + frame_margin,
                              rows_y - frame_margin,
                              "/\\")
        self.buttons_list.append(self.rows_up)

        self.rows_dn = Button(rows_x - frame_margin,
                              rows_y + frame_margin,
                              rows_x + frame_margin,
                              rows_y +  (2 * frame_margin),
                              "\/")
        self.buttons_list.append(self.rows_dn)

        self.audio = Button((self.width * 0.9),
                      0,
                      self.width,
                      (self.gui_size * 0.4),
                      '')
        self.buttons_list.append(self.audio)

    def generate_level(self, how_many_columns: int, how_many_rows: int) -> list:
        
        """
        ______________________________________________________________________

        how_many_columns, how_many_rows: <int>


        ---> <list> --> [<list>, <list>, ... , <list>]
        ______________________________________________________________________

        Return a list of lists which is the grid of the grid with its indexes.
        """

        grid = [[None] + [list() for _ in range(how_many_columns)]]

        for _ in range(how_many_rows):

            temp_list = [list()]

            for _ in range(how_many_columns):

                temp_list.append([choice((False, True)), True])
            
            grid.append(temp_list)

        return self.generate_index(grid)

    def generate_index(self, grid: list) -> list:
        """
        ______________________________________________________________________

        grid: <list> --> [<list>, <list>, ... , <list>]


        ---> <list> --> [<list>, <list>, ... , <list>]
        ______________________________________________________________________

        Receives a list of lists which is the grid of the game, processes it and
        writes the indexes according to its columns and rows.
        """

        cols, rows = len(grid[0]), len(grid)

        for col_index in range(1, cols):

            column = column_list(grid, col_index, with_index=False)
            filtered_column = [len(elem) for elem in split_filter(column, (lambda elem: elem[0]))]

            grid[0][col_index] = (filtered_column if filtered_column else [0])

        for row_index in range(1, rows):

            row = row_list(grid, row_index, with_index=False)
            filtered_row = [len(elem) for elem in split_filter(row, (lambda elem: elem[0]))]

            grid[row_index][0] = (filtered_row if filtered_row else [0])

        return grid

    def dimensions(self) -> list[int, int]:
        """
        Returns the dimensions of the game grid (NOT those of the window).
        """

        return (len(self.grid[0]), len(self.grid))

    def calculate_indexes(self) -> tuple[int, int]:
        """
        Returns a tuple which is the calculated spaces dedicated to the index cells.
        """

        return (self.width / 5), (self.height / 7)

    def calculate_playable_area(self) -> tuple[int, int, int, int]:
        """
        Returns a tuple which is the cornes of the area dedicated to the clickable cells.
        """

        index_x, index_y = self.calculate_indexes()

        return (index_x, (index_y + self.gui_size), self.width, self.height)

    def calculate_coords(self, x: int, y: int) -> tuple[int, int]:
        """
        Given a pair of coordinates, it traces it back to the grid and calculates whose
        cell it belongs to.
        
        Returns a tuple of two integers.
        """

        cols, rows = self.dimensions()
        index_x, index_y = self.calculate_indexes()

        cell_x = (self.width - index_x) / (cols - 1)
        cell_y = (self.height - index_y - self.gui_size) / (rows - 1)

        return int((x - index_x) / cell_x) + 1, int((y - index_y - self.gui_size) / cell_y) + 1

    def process_click(self, x: int, y: int, event_type: int) -> None:
        """
        Given the coordinates of a click action and the type of button pressed, it
        gets processed into its corresponding action.

        'event_type' is meant to be always 1, 2 or 3, but only '1 or else' is processed.
        """

        area_x1, area_y1, area_x2, area_y2 = self.calculate_playable_area()

        if area_x1 <= x <= area_x2 and area_y1 <= y <= area_y2:

            x_coord, y_coord = self.calculate_coords(x, y)

            cell = self.grid[y_coord][x_coord]

            if cell[1]:

                if (not cell[0] if event_type == 1 else cell[0]):

                    self.mistakes_count += 1
                    self.mistakes_coord.append((x_coord, y_coord))
                    if self.has_audio: gamelib.play_sound("gamelibgames/picross/sfx/tile_wrong.wav")
                
                else:

                    if self.has_audio: gamelib.play_sound("gamelibgames/picross/sfx/tile_right.wav")

                cell[1] = False

        else:

            for button in self.buttons_list:

                if button.is_inside(x, y):

                    if button is self.new_game:

                        self.start_new_game()

                    elif button is self.cols_up:

                        self.grid_x += 1

                    elif button is self.cols_dn:

                        self.grid_x = ((self.grid_x - 1) if self.grid_x > 4 else self.grid_x)

                    elif button is self.rows_up:

                        self.grid_y += 1

                    elif button is self.rows_dn:

                        self.grid_y = ((self.grid_y - 1) if self.grid_y > 4 else self.grid_y)

                    elif button is self.audio:

                        self.has_audio = not self.has_audio

                    break

    def did_it_end(self) -> tuple[bool, bool]:
        """
        It determines if the game has ended, and if so, if the player won or not.

        The first boolean is to determine if the game ended or not.

        The second boolean is to determine if it was a victory ('False' by default,
        if the game hasn't ended yet).
        """

        cols, rows = self.dimensions()

        if self.mistakes_count >= self.max_mistakes:

            return True, False

        for x in range(1, cols):

            for y in range(1, rows):

                is_filled, is_hidden = self.grid[y][x]

                if (True if self.has_to_clear_grid else is_filled) and is_hidden:

                    return False, False
        
        return True, True

    def advance_game(self) -> None:
        """
        Avances the state of the game, updating the corresponding attributes if
        necessary.
        """

        game_ended, is_victory = self.did_it_end()

        if game_ended:

            self.ended = True

            if self.has_audio: gamelib.play_sound("gamelibgames/picross/sfx/game_won.wav" if is_victory else "gamelibgames/picross/sfx/game_lost.wav")
            gamelib.say("You Won!" if is_victory else "You Lost!")

            answer = gamelib.input("Another Round? (y/n)")

            if answer == 'y':

                self.start_new_game()

    def start_new_game(self) -> None:
        """
        Modifies certain game attributes so a new grid is generated with the
        given modifiable values, and also resets the mistakes count, the coordinates
        list, and sets the game to 'not ended'.
        """

        self.ended = False
        self.mistakes_count = 0
        self.mistakes_coord = list()

        self.grid = self.generate_level(self.grid_x, self.grid_y)


def main() -> None:
    """
    This function is meant to be called once and just once, with the execution
    of the program.
    """

    game = PicrossGame(WIDTH, HEIGHT)

    gamelib.title(f"Simple Picross by NLGS")
    gamelib.resize(game.width, game.height)
    gamelib.icon("gamelibgames/picross/img/icon/picross_logo.gif")

    while gamelib.loop(fps=60):

        if game.ended:

            break

        gamelib.draw_begin()
        graphics.draw_screen(game)
        gamelib.draw_end()

        event = gamelib.wait(gamelib.EventType.ButtonPress)

        game.process_click(event.x, event.y, event.mouse_button)

        game.advance_game()

if __name__ == "__main__":

    gamelib.init(main)