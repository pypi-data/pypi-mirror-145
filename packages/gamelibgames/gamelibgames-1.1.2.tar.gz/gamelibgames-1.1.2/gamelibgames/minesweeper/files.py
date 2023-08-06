"""
This module manages all text files, and stores function related
to reading or writing in them.
"""


def map_color_profiles(file_name: str="gamelibgames/minesweeper/color_profiles.txt") -> dict:
    """
    ______________________________________________________________________

    file_name: <str>


    ---> <dict> --> {<str> : <dict>*, <str> : <dict>*, ... , <str> : <dict>*}

        *<dict> --> {<str> : <str>, <str> : <str>, ... , <str> : <str>}
    ______________________________________________________________________

    Returns a dictionary with other dictionaries as its values which stores the
    color values for each personalized color profile.
    """

    profiles_dict = dict()
    current_name = ''

    with open(file_name) as file:

        for line in file:

            if line == '\n' or line[0] == '#': # line defines a comment

                continue

            type, key, *value = ''.join(line.split('=')).split()

            if type == "!t": # line defines a new Profile

                profiles_dict[key] = dict()
                current_name = key

            elif type == "!v": # line defines a 'key-value' pair

                value = ''.join(value)
                profiles_dict[current_name][key] = (value if not value == '/' else '')

    return profiles_dict

def map_figures(file_name: str="gamelibgames/minesweeper/figures.txt") -> dict:
    """
    ______________________________________________________________________

    file_name: <str>


    ---> <dict> --> {<str> : <dict>*, <str> : <dict>*, ... , <str> : <dict>*}

        *<dict> --> {<tuple>** : <str>, <tuple>** : <str>, ... , <tuple>** : <str>}

        **<tuple> --> (<int>, <int>)
    ______________________________________________________________________

    Returns a dictionary with other dictionaries as its values which stores the
    color values for each pixel in a defined area of a figure.
    """

    figures_dict = dict()
    current_figure = ''

    figure_list = list()
    searching_in_list = False

    with open(file_name) as file:

        for line in file:

            if line == '\n' or line[0] == '#': # line is empty or defines a comment

                continue

            fragmented_line = line.rstrip().split()

            if searching_in_list and not fragmented_line[0] == "/>":

                figure_list.append(fragmented_line)

            if fragmented_line[0] == "!f":

                name = fragmented_line[1]

                figures_dict[name] = dict()
                current_figure = name

            elif fragmented_line[0] == "!<":

                figure_list = list()
                searching_in_list = True

            elif fragmented_line[0] == "/>":

                for px_x in range(len(figure_list[0])):

                    for px_y in range(len(figure_list)):

                        pixel = figure_list[px_y][px_x]

                        if not pixel == '.':

                            figures_dict[current_figure][(px_x, px_y)] = pixel

                searching_in_list = False

    return figures_dict