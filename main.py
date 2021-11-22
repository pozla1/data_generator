import time

import add_education
import check
import generate_agents
import rw


# ********** SETTINGS **********

# Set input file names
residences_filename = "szeged_respoi.json"
magics_filename_generation = "szeged_magic_numbers_original.json"
magics_filename_check = "szeged_magic_numbers_original.json"
misc_consts_filename = "misc_constants.json"
educational_institutions_filename = "educational_institutions.xls"
creches_filename = "creches.xls"
schools_filename = "schools.xls"
locality_filter = "Csongrád"

# Set output file name
output_filename = "input_data"

# Set desired features
_generate_agents = True
_add_education = True
_check = True
_clean_up = True  # Should be run every time


# ********** SCRIPT **********

# Save start time
start_time = time.localtime()

# Format output file names
output_filename += "_"
output_filename += time.strftime("%Y%m%d_%H%M%S", start_time)
report_filename = output_filename + "_report.txt"
# seeds_filename = output_filename + "_seeds.txt"
output_filename += ".json"


# Main agents array
agents = []


# Generate desired features
if _generate_agents:
    agents = generate_agents.generate_agents(agents, residences_filename, magics_filename_generation,
                                             misc_consts_filename, report_filename)
if _add_education:
    agents = add_education.add_education(agents, educational_institutions_filename, creches_filename, schools_filename,
                                         locality_filter, misc_consts_filename, report_filename)

# Save finish time
finish_time = time.localtime()


# Write to report
rw.append_to_file("!output_files\\" + report_filename,
                  "Time:\n" +
                  "    Start: " + str(time.strftime("%Y.%m.%d. %H:%M:%S", start_time)) + "\n" +
                  "    Finish: " + str(time.strftime("%Y.%m.%d. %H:%M:%S", finish_time)) + "\n")


# Run check
if _check:
    check.check_agents(agents, magics_filename_check, misc_consts_filename, report_filename)

# Run cleanup
if _clean_up:
    check.clean_up(agents, report_filename)


# Write out generated agents
agents = {"people": agents}
rw.write_to_json("!output_files\\" + output_filename, agents)
