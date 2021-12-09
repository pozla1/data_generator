import generate_family
import rw


# Generates agents for residence data
def generate_agents(agents, residences_filename, magics_filename, misc_consts_filename, report_filename):

    # Load and sort cells
    cells = rw.load_from_json("!input_files\\" + residences_filename)
    cells = cells["places"]
    cells = sort_by_capacity(cells)

    # Load input data
    magics = rw.load_from_json("!input_files\\" + magics_filename)
    misc_consts = rw.load_from_json("!input_files\\" + misc_consts_filename)

    # For progress logging
    num_of_cells = len(cells)
    _sum = 0
    population = 0
    for cell in cells:
        population += cell["capacity"]

    # Generate families and put them in a cell
    fam_id = 1
    while len(cells) > 0:

        # Generate a family and calculate its properties
        generated_agents = generate_family.generate_family(fam_id, magics, misc_consts)
        number_of_agents = len(generated_agents)
        age_distribution = get_age_distribution(generated_agents, misc_consts["age_groups"])

        # Find an appropriate cell for the generated family
        for cell in cells:

            # Decide if it fits
            if cell["capacity"] >= number_of_agents \
                    and check_age_distribution(cell["ageDistribution"], age_distribution):

                # If yes, save cell data into agents properties and append agents to the main agents array
                for agent in generated_agents:
                    agent["locations"] = {"typeID": 2, "locID": cell["id"]}
                    agents.append(agent)

                # Refresh cell properties and sort again
                cell["capacity"] -= number_of_agents
                cell["ageDistribution"] = modify_age_distribution(cell["ageDistribution"], age_distribution)
                cells = sort_by_capacity(cells)

                # If cell capacity reaches 0, remove it
                if cell["capacity"] == 0:
                    cells.remove(cell)

                # Log progress to console
                _sum = 0
                for _cell in cells:
                    _sum += _cell["capacity"]
                print("Progress: " + str(len(cells)) + "/" + str(num_of_cells) + " cells and "
                      + str(_sum) + "/" + str(population) + " agents remaining.")

                # If fitting cell found, break, and continue with the next generated family
                fam_id += 1
                break

        # If no agents can be placed (without 'other' family type), stop
        is_end = True
        for cell in cells:
            if not (cell["ageDistribution"][2] == 0 and cell["ageDistribution"][3] == 0
                    and cell["ageDistribution"][4] == 0):
                is_end = False
                break
        if is_end:
            break

    # Write to report
    rw.append_to_file("!output_files\\" + report_filename,
                      "Generation: " + str(num_of_cells - len(cells)) + "/" + str(num_of_cells) + " cells filled and "
                      + str(population - _sum) + "/" + str(population) + " agents generated.\n")

    return agents


# Sort cells by capacity
def sort_by_capacity(cells):
    cells = sorted(cells, key=lambda k: k["capacity"])
    return cells


# Returns the age distribution of given agents
def get_age_distribution(agents, age_groups):
    age_distribution = [0, 0, 0, 0, 0]
    for agent in agents:
        if age_groups[0][0] <= agent["age"] <= age_groups[0][1]:
            age_distribution[0] += 1
        elif age_groups[1][0] <= agent["age"] <= age_groups[1][1]:
            age_distribution[1] += 1
        elif age_groups[2][0] <= agent["age"] <= age_groups[2][1]:
            age_distribution[2] += 1
        elif age_groups[3][0] <= agent["age"] <= age_groups[3][1]:
            age_distribution[3] += 1
        else:
            age_distribution[4] += 1
    return age_distribution


# Decides if values in distrib1 are greater or equal to values in distrib2
def check_age_distribution(distrib1, distrib2):
    if distrib1[0] >= distrib2[0] and distrib1[1] >= distrib2[1] and distrib1[2] >= distrib2[2] \
            and distrib1[3] >= distrib2[3] and distrib1[4] >= distrib2[4]:
        return True
    else:
        return False


# Subtracts values in distrib2 from values in distrib1
def modify_age_distribution(distrib1, distrib2):
    distrib1[0] -= distrib2[0]
    distrib1[1] -= distrib2[1]
    distrib1[2] -= distrib2[2]
    distrib1[3] -= distrib2[3]
    distrib1[4] -= distrib2[4]
    return [distrib1[0], distrib1[1], distrib1[2], distrib1[3], distrib1[4]]
