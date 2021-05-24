import time

import check
import generate_agents
import rw


# Save start time
start_time = time.localtime()


# Set input file names
residences_filename = "szeged_respoi.json"
magics_filename_generation = "szeged_magic_numbers_tuned.json"
magics_filename_check = "szeged_magic_numbers_original.json"
misc_consts_filename = "misc_constants.json"

# Set output file name
output_filename = "input_data"


# Format output file names
output_filename += "_"
output_filename += time.strftime("%Y%m%d_%H%M%S", start_time)
report_filename = output_filename + "_report.txt"
# seeds_filename = output_filename + "_seeds.txt"
output_filename += ".json"


# Main agents array
agents = []

# Generate desired features
agents = generate_agents.generate_agents(agents, residences_filename, magics_filename_generation, misc_consts_filename,
                                         report_filename)

# Save finish time
finish_time = time.localtime()


# Write to report
rw.append_to_file("!output_files\\" + report_filename,
                  "Time:\n" +
                  "    Start: " + str(time.strftime("%Y.%m.%d. %H:%M:%S", start_time)) + "\n" +
                  "    Finish: " + str(time.strftime("%Y.%m.%d. %H:%M:%S", finish_time)) + "\n")


# Run desired checking methods
check.check_agents(agents, magics_filename_check, misc_consts_filename, report_filename)

# Cleanup should be run every time
check.clean_up(agents, report_filename)


# Write out generated agents
agents = {"people": agents}
rw.write_to_json("!output_files\\" + output_filename, agents)
