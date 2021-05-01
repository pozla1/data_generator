import random
import generate_families


output_filename = "input_data_01"
seeds_filename = output_filename + "_seeds.txt"
output_filename += ".json"


generate_families.generate_families(output_filename, seeds_filename)
