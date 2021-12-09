import rw


# Checks if generated agents fit the statistics.
def check_agents(agents, magics_filename, misc_consts_filename, report_filename):

    # Load input data
    magics = rw.load_from_json("!input_files\\" + magics_filename)
    misc_consts = rw.load_from_json("!input_files\\" + misc_consts_filename)

    # Create arrays filled with zeros, representing magic numbers
    fam_type = [0, 0, 0, 0]
    elderly_num = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    child_num = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    child_age = [[0, 0, 0, 0], [0, 0, 0, 0]]
    single_type = [0, 0]
    parent_type = [[0, 0], [0, 0], [0, 0], [0, 0]]
    age_distrib = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Separate families by family ID
    families = {}
    for agent in agents:
        family = []
        families[agent["for_check"]["family_ID"]] = family
    for agent in agents:
        families[agent["for_check"]["family_ID"]].append(agent)

    # Fill previously created arrays
    for family in families:
        _elderly_num = 0
        _child_num = 0

        # Get and set family type
        _fam_type = families[family][0]["for_check"]["family_type"]
        fam_type[_fam_type] += 1

        for agent in families[family]:
            # Get number of elderly
            if agent["for_check"]["agent_type"] == "elderly":
                _elderly_num += 1
            # Get number of children
            if agent["for_check"]["agent_type"][:-1] == "child":
                _child_num += 1
                # Get and set child age
                child_age[_fam_type - 2][int(agent["for_check"]["agent_type"][-1])] += 1
            # Get and set single type
            if agent["for_check"]["agent_type"][:-1] == "single":
                single_type[int(agent["for_check"]["agent_type"][-1])] += 1
            # Get and set parent type
            if agent["for_check"]["agent_type"][:-1] == "parent":
                parent_type[_fam_type][int(agent["for_check"]["agent_type"][-1])] += 1

        # Set number of elderly
        elderly_num[_fam_type][_elderly_num] += 1
        # Set number of children
        child_num[_fam_type][_child_num] += 1

    # Normalize vectors
    fam_type = normalize(fam_type)
    for row in elderly_num:
        row = normalize(row)
    for row in child_num:
        row = normalize(row)
    for row in child_age:
        row = normalize(row)
    single_type = normalize(single_type)
    for row in parent_type:
        row = normalize(row)

    # Create vectors with differences
    fam_type_diff = create_diff(magics["fam_type"], fam_type)
    elderly_num_diff = []
    for i in range(len(elderly_num)):
        elderly_num_diff.append(create_diff(magics["elderly_num"][i], elderly_num[i]))
    child_num_diff = []
    for i in range(len(child_num)):
        child_num_diff.append(create_diff(magics["child_num"][i], child_num[i]))
    child_age_diff = []
    for i in range(len(child_age)):
        child_age_diff.append(create_diff(magics["child_age"][i], child_age[i]))
    single_type_diff = create_diff(magics["single_type"], single_type)
    parent_type_diff = []
    for i in range(len(parent_type)):
        parent_type_diff.append(create_diff(magics["parent_type"][i], parent_type[i]))

    # Write to report
    rw.append_to_file("!output_files\\" + report_filename,
                      "Agents check:\n" +
                      "    " + magics["fam_type_comment"] + ":\n" +
                      "        Original: " + str(magics["fam_type"]) + "\n" +
                      "        Generated: " + str(fam_type) + "\n" +
                      "        Difference in %: " + str(fam_type_diff) + "\n" +
                      "    " + magics["elderly_num_comment"] + ":\n" +
                      "        Original: " + str(magics["elderly_num"]) + "\n" +
                      "        Generated: " + str(elderly_num) + "\n" +
                      "        Difference in %: " + str(elderly_num_diff) + "\n" +
                      "    " + magics["child_num_comment"] + ":\n" +
                      "        Original: " + str(magics["child_num"]) + "\n" +
                      "        Generated: " + str(child_num) + "\n" +
                      "        Difference in %: " + str(child_num_diff) + "\n" +
                      "    " + magics["child_age_comment"] + ":\n" +
                      "        Original: " + str(magics["child_age"]) + "\n" +
                      "        Generated: " + str(child_age) + "\n" +
                      "        Difference in %: " + str(child_age_diff) + "\n" +
                      "    " + magics["single_type_comment"] + ":\n" +
                      "        Original: " + str(magics["single_type"]) + "\n" +
                      "        Generated: " + str(single_type) + "\n" +
                      "        Difference in %: " + str(single_type_diff) + "\n" +
                      "    " + magics["parent_type_comment"] + ":\n" +
                      "        Original: " + str(magics["parent_type"]) + "\n" +
                      "        Generated: " + str(parent_type) + "\n" +
                      "        Difference in %: " + str(parent_type_diff) + "\n")


# Returns the given vector normalized.
def normalize(vector):
    _sum = 0
    for i in range(len(vector)):
        _sum += vector[i]
    for i in range(len(vector)):
        if _sum != 0:
            vector[i] /= _sum
    return vector


# Creates a vector with % values between given vectors
def create_diff(vector1, vector2):
    _diff = []
    for i in range(len(vector1)):
        if vector1[i] == 0 and vector2[i] == 0:
            _diff.append(0)
        elif vector1[i] == 0:
            _diff.append("+inf")
        elif vector2[i] == 0:
            _diff.append("-inf")
        else:
            _diff.append(vector2[i] / vector1[i] * 100 - 100)
    return _diff


# Removes the 'for_check' attribute from given agents
def clean_up(agents, report_filename):
    for agent in agents:
        del agent["for_check"]

    rw.append_to_file("!output_files\\" + report_filename,
                      "Cleanup: \'for-check\' attribute removed.\n")
