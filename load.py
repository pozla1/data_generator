import json


def load_magics():
    magics_filename = "szeged_magic_numbers.json"
    with open(magics_filename, "r") as magics_file:
        magics = json.load(magics_file)
    return magics

# todo: other loader functions will be implemented here
