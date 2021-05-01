import json

import generate_families


output_filename = "input_data_01"
magics_filename = "szeged_magic_numbers.json"

seeds_filename = output_filename + "_seeds.txt"
output_filename += ".json"


agents = []

generate_families.generate_families(magics_filename, seeds_filename, agents)

agents = {"people": agents}


with open(output_filename, "w") as output_file:
    json.dump(agents, output_file, indent="\t")
