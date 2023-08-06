"""
This module manages all text files, and stores function related
to reading or writing in them.
"""

def map_color_profiles(file_name: str="gamelibgames/picross/color_profiles.txt") -> dict:
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
