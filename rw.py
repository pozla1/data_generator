import json


# Returns data loaded from given json file.
def load_from_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


# Writes given data to given json file.
def write_to_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent="\t")


# Appends given data to given file.
def append_to_file(filename, data):
    with open(filename, "a") as file:
        file.write(str(data) + "\n")
