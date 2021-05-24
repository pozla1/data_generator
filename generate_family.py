import random


# Generates a family
def generate_family(fam_id, magics, misc_consts):

    # Agents array for generated family members
    agents = []

    # Decide family type
    rand = random.random()

    # Single person family
    if rand <= magics["fam_type"][0]:
        # Decide if elderly or not
        rand = random.random()
        # Not elderly
        if rand < magics["elderly_num"][0][0]:
            # Decide if younger single or older single
            rand = random.random()
            # Younger single
            if rand < magics["single_type"][0]:
                agent_type = "single0"
                min_age = misc_consts["age_groups"][2][0]
                max_age = misc_consts["age_groups"][2][1]
            # Older single
            else:
                agent_type = "single1"
                min_age = misc_consts["age_groups"][3][0]
                max_age = misc_consts["age_groups"][3][1]
        # Elderly
        else:
            agent_type = "elderly"
            min_age = misc_consts["age_groups"][4][0]
            max_age = misc_consts["age_groups"][4][1]

        agent = {"for_check": {"family_ID": fam_id, "family_type": 0, "agent_type": agent_type},
                 "age": generate_age(min_age, max_age, magics["age_distrib"]),
                 "sex": generate_sex()}
        agents.append(agent)

    # Family with 1 parent or 2 parents
    elif rand <= magics["fam_type"][0] + magics["fam_type"][1] + magics["fam_type"][2]:
        # Family with 1 parent
        if rand <= magics["fam_type"][0] + magics["fam_type"][1]:
            family_type = 1
        # Family with 2 parents
        else:
            family_type = 2

        # Get number of children
        rand = random.random()
        if rand <= magics["child_num"][family_type][0]:
            num_of_children = 0
        elif rand <= magics["child_num"][family_type][0] + magics["child_num"][family_type][1]:
            num_of_children = 1
        elif rand <= magics["child_num"][family_type][0] + magics["child_num"][family_type][1]\
                + magics["child_num"][family_type][2]:
            num_of_children = 2
        else:
            num_of_children = 3  # todo: 3+

        # Get children age
        min_age_children = 0
        max_age_children = 0
        if num_of_children != 0:
            while True:
                age_diff_children = random.randint(misc_consts["age_diff_children"][0],
                                                   misc_consts["age_diff_children"][1])
                children_age_intervals = []
                for i in range(num_of_children):
                    rand = random.random()
                    if rand <= magics["child_age"][family_type - 1][0]:
                        children_age_intervals.append([misc_consts["age_groups"][0][0],
                                                       misc_consts["age_groups"][0][1]])
                    elif rand <= magics["child_age"][family_type - 1][0] + magics["child_age"][family_type - 1][1]:
                        children_age_intervals.append([misc_consts["age_groups"][1][0],
                                                       misc_consts["age_groups"][1][1]])
                    elif rand <= magics["child_age"][family_type - 1][0] + magics["child_age"][family_type - 1][1]\
                            + magics["child_age"][family_type - 1][2]:
                        children_age_intervals.append([misc_consts["age_groups"][2][0],
                                                       misc_consts["age_groups"][2][1]])
                    else:
                        children_age_intervals.append([misc_consts["age_groups"][3][0],
                                                       misc_consts["age_groups"][3][1]])

                children_ages = []
                for age_interval in children_age_intervals:
                    children_ages.append(generate_age(age_interval[0], age_interval[1], magics["age_distrib"]))

                min_age_children = children_ages[0]
                max_age_children = children_ages[0]
                for age in children_ages:
                    if min_age_children < age:
                        min_age_children = age
                    if max_age_children > age:
                        max_age_children = age

                if max_age_children - min_age_children <= age_diff_children:
                    break

            for age in children_ages:
                agent = {"for_check": {"family_ID": fam_id, "family_type": family_type,
                                       "agent_type": get_child_type(age, misc_consts)},
                         "age": age,
                         "sex": generate_sex()}
                agents.append(agent)

        # Generate parents
        while True:
            age_diff_parents = random.randint(misc_consts["age_diff_parents"][0], misc_consts["age_diff_parents"][1])
            age_diff_gen = random.randint(misc_consts["age_diff_gen"][0], misc_consts["age_diff_gen"][1])
            parents_age_intervals = []
            for i in range(family_type):
                rand = random.random()
                if rand <= magics["parent_type"][num_of_children][0]:
                    parents_age_intervals.append([misc_consts["age_groups"][2][0], misc_consts["age_groups"][2][1]])
                else:
                    parents_age_intervals.append([misc_consts["age_groups"][3][0], misc_consts["age_groups"][3][1]])

            parents_ages = []
            for age_interval in parents_age_intervals:
                parents_ages.append(generate_age(age_interval[0], age_interval[1], magics["age_distrib"]))

            min_age_parents = parents_ages[0]
            max_age_parents = parents_ages[0]
            for age in parents_ages:
                if min_age_parents < age:
                    min_age_parents = age
                if max_age_parents > age:
                    max_age_parents = age

            if max_age_parents - min_age_parents <= age_diff_parents \
                    and min_age_parents - max_age_children <= age_diff_gen:
                break

        if len(parents_ages) == 1:
            agent = {"for_check": {"family_ID": fam_id, "family_type": family_type,
                                   "agent_type": get_parent_type(parents_ages[0], misc_consts)},
                     "age": parents_ages[0],
                     "sex": generate_sex()}
            agents.append(agent)
        elif parents_ages[0] >= parents_ages[1]:  # todo? father always older
            agent = {"for_check": {"family_ID": fam_id, "family_type": family_type,
                                   "agent_type": get_parent_type(parents_ages[0], misc_consts)},
                     "age": parents_ages[0],
                     "sex": "M"}
            agents.append(agent)
            agent = {"for_check": {"family_ID": fam_id, "family_type": family_type,
                                   "agent_type": get_parent_type(parents_ages[1], misc_consts)},
                     "age": parents_ages[1],
                     "sex": "F"}
            agents.append(agent)
        else:
            agent = {"for_check": {"family_ID": fam_id, "family_type": family_type,
                                   "agent_type": get_parent_type(parents_ages[1], misc_consts)},
                     "age": parents_ages[1],
                     "sex": "M"}
            agents.append(agent)
            agent = {"for_check": {"family_ID": fam_id, "family_type": family_type,
                                   "agent_type": get_parent_type(parents_ages[0], misc_consts)},
                     "age": parents_ages[0],
                     "sex": "F"}
            agents.append(agent)

        # Generate elderly
        rand = random.random()
        if rand <= magics["elderly_num"][family_type][0]:
            num_of_elderly = 0
        elif rand <= magics["elderly_num"][family_type][0] + magics["elderly_num"][family_type][1]:
            num_of_elderly = 1
        elif rand <= magics["elderly_num"][family_type][0] + magics["elderly_num"][family_type][1] \
                + magics["elderly_num"][family_type][2]:
            num_of_elderly = 2
        else:
            num_of_elderly = 3  # todo: 3+

        for i in range(num_of_elderly):
            agent = {"for_check": {"family_ID": fam_id, "family_type": family_type, "agent_type": "elderly"},
                     "age": generate_age(misc_consts["age_groups"][4][0], misc_consts["age_groups"][4][1],
                                         magics["age_distrib"]),
                     "sex": generate_sex()}
            agents.append(agent)

    # todo
    """
    # 'Other' family type
    else:
        pass
    """

    return agents


# Returns the generated age between given minimum and maximum value.
def generate_age(min_age, max_age, age_distrib):
    rand = random.random()
    age_interval = get_age_group(rand, age_distrib)
    while not (min_age <= age_interval[1] and age_interval[0] <= max_age):
        rand = random.random()
        age_interval = get_age_group(rand, age_distrib)
    rand = random.randint(age_interval[0], age_interval[1])
    while not (min_age <= rand <= max_age):
        rand = random.randint(age_interval[0], age_interval[1])
    return rand


# Returns the appropriate age interval for given random value between 0-1.
def get_age_group(rand, age_distrib):
    value1 = age_distrib[0]
    value2 = value1 + age_distrib[1]
    value3 = value2 + age_distrib[2]
    value4 = value3 + age_distrib[3]
    value5 = value4 + age_distrib[4]
    value6 = value5 + age_distrib[5]
    value7 = value6 + age_distrib[6]
    value8 = value7 + age_distrib[7]
    value9 = value8 + age_distrib[8]
    value10 = value9 + age_distrib[9]
    value11 = value10 + age_distrib[10]
    value12 = value11 + age_distrib[11]
    value13 = value12 + age_distrib[12]
    value14 = value13 + age_distrib[13]
    value15 = value14 + age_distrib[14]
    value16 = value15 + age_distrib[15]
    value17 = value16 + age_distrib[16]

    if rand <= value1:
        age_interval = [0, 3]  # todo: load these numbers from file
    elif rand <= value2:
        age_interval = [4, 8]
    elif rand <= value3:
        age_interval = [9, 13]
    elif rand <= value4:
        age_interval = [14, 18]
    elif rand <= value5:
        age_interval = [19, 23]
    elif rand <= value6:
        age_interval = [24, 28]
    elif rand <= value7:
        age_interval = [29, 33]
    elif rand <= value8:
        age_interval = [34, 38]
    elif rand <= value9:
        age_interval = [39, 43]
    elif rand <= value10:
        age_interval = [44, 48]
    elif rand <= value11:
        age_interval = [49, 53]
    elif rand <= value12:
        age_interval = [54, 58]
    elif rand <= value13:
        age_interval = [59, 63]
    elif rand <= value14:
        age_interval = [64, 68]
    elif rand <= value15:
        age_interval = [69, 73]
    elif rand <= value16:
        age_interval = [74, 78]
    elif rand <= value17:
        age_interval = [79, 83]
    else:
        age_interval = [84, 90]

    return age_interval


# Returns generated sex.  # todo: implement real sex distribution
def generate_sex():
    rand = random.randint(0, 1)
    if rand == 0:
        return "F"
    else:
        return "M"


# Returns the type of child with given age.
def get_child_type(age, misc_consts):
    if misc_consts["age_groups"][0][0] <= age <= misc_consts["age_groups"][0][1]:
        return "child0"
    elif misc_consts["age_groups"][1][0] <= age <= misc_consts["age_groups"][1][1]:
        return "child1"
    elif misc_consts["age_groups"][2][0] <= age <= misc_consts["age_groups"][2][1]:
        return "child2"
    else:
        return "child3"


# Returns the type of child with given age.
def get_parent_type(age, misc_consts):
    if misc_consts["age_groups"][2][0] <= age <= misc_consts["age_groups"][2][1]:
        return "parent0"
    else:
        return "parent1"
