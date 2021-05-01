import json


# Returns magic numbers loaded from given file.
def load_magics(magics_filename):
    with open(magics_filename, "r") as magics_file:
        magics = json.load(magics_file)
    return magics


# todo: other loader functions will be implemented here
