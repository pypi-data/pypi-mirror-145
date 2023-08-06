from .gamelib import init as game_init
from .picross import main as picross_main
from .minesweeper import main as minesweeper_main

__version__ = "1.1.1"

ACCEPTED_VALUES = 'picross', 'minesweeper'

def main(argv) -> None:

    if not argv or argv[0] not in ACCEPTED_VALUES:

        print(f"Game Name Invalid. Please use one of the following:\n{ACCEPTED_VALUES}")
        return

    game_chosen: str = argv[0]

    if game_chosen == 'picross':

        game_init(picross_main)

    elif game_chosen == 'minesweeper':

        game_init(minesweeper_main)


if __name__ == '__main__':

    main()
