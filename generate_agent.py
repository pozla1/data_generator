import random


# Generates a single type agent with age and sex.
def generate_single(agents, fam_id, magics):

    # generate age
    rand = random.random()
    if rand < magics["single_type"][0]:
        # younger single
        min_age = 18  # todo: age interval correct?
        max_age = 29
        age = generate_age(min_age, max_age, magics)
    else:
        # older single
        min_age = 30
        max_age = 64
        age = generate_age(min_age, max_age, magics)

    # generate sex
    sex = generate_sex()

    # generate agent
    generate_agent(agents, fam_id, age, sex)


# Generates an elderly type agent with age and sex.
def generate_elderly(agents, fam_id, magics):

    # generate age
    min_age = 65  # todo: age interval correct?
    max_age = 100
    age = generate_age(min_age, max_age, magics)

    # generate sex
    sex = generate_sex()

    # generate agent
    generate_agent(agents, fam_id, age, sex)


# Generates a parent type agent with age and sex.
def generate_parent(agents, fam_id, magics, parent_type, _sex):

    # generate age
    rand = random.random()
    if rand < magics["parent_type"][parent_type][0]:
        min_age = 18  # todo: age interval correct?
        max_age = 29
        age = generate_age(min_age, max_age, magics)
    else:
        min_age = 30
        max_age = 64
        age = generate_age(min_age, max_age, magics)

    # generate sex
    if _sex == "random":
        sex = generate_sex()
    else:
        sex = _sex

    # generate agent
    generate_agent(agents, fam_id, age, sex)


# Generates a child type agent with age and sex.
def generate_child(agents, fam_id, magics):
    # todo: magic4? age distrib for children, but no values + why 2 rows?

    # generate age
    min_age = 0  # todo: age interval correct?
    max_age = 18
    age = generate_age(min_age, max_age, magics)

    # generate sex
    sex = generate_sex()

    # generate agent
    generate_agent(agents, fam_id, age, sex)


# Returns the appropriate age interval for given random value between 0-1.
def get_age_group(rand, magics):
    value1 = magics["age_distrib"][0]
    value2 = value1 + magics["age_distrib"][1]
    value3 = value2 + magics["age_distrib"][2]
    value4 = value3 + magics["age_distrib"][3]
    value5 = value4 + magics["age_distrib"][4]
    value6 = value5 + magics["age_distrib"][5]
    value7 = value6 + magics["age_distrib"][6]
    value8 = value7 + magics["age_distrib"][7]
    value9 = value8 + magics["age_distrib"][8]
    value10 = value9 + magics["age_distrib"][9]
    value11 = value10 + magics["age_distrib"][10]
    value12 = value11 + magics["age_distrib"][11]
    value13 = value12 + magics["age_distrib"][12]
    value14 = value13 + magics["age_distrib"][13]
    value15 = value14 + magics["age_distrib"][14]
    value16 = value15 + magics["age_distrib"][15]
    value17 = value16 + magics["age_distrib"][16]

    if rand < value1:
        age_interval = [0, 3]
    elif rand < value2:
        age_interval = [4, 8]
    elif rand < value3:
        age_interval = [9, 13]
    elif rand < value4:
        age_interval = [14, 18]
    elif rand < value5:
        age_interval = [19, 23]
    elif rand < value6:
        age_interval = [24, 28]
    elif rand < value7:
        age_interval = [29, 33]
    elif rand < value8:
        age_interval = [34, 38]
    elif rand < value9:
        age_interval = [39, 43]
    elif rand < value10:
        age_interval = [44, 48]
    elif rand < value11:
        age_interval = [49, 53]
    elif rand < value12:
        age_interval = [54, 58]
    elif rand < value13:
        age_interval = [59, 63]
    elif rand < value14:
        age_interval = [64, 68]
    elif rand < value15:
        age_interval = [69, 73]
    elif rand < value16:
        age_interval = [74, 78]
    elif rand < value17:
        age_interval = [79, 83]
    else:
        age_interval = [84, 100]  # todo: max age?

    return age_interval


# Returns the generated age between given minimum and maximum value.
def generate_age(min_age, max_age, magics):
    rand = random.random()
    age_interval = get_age_group(rand, magics)
    while not (min_age <= age_interval[1] and age_interval[0] <= max_age):
        rand = random.random()
        age_interval = get_age_group(rand, magics)
    rand = random.randint(age_interval[0], age_interval[1])
    while not (min_age <= rand <= max_age):
        rand = random.randint(age_interval[0], age_interval[1])
    return rand


# Returns generated sex.
def generate_sex():
    rand = random.randint(0, 1)  # todo: correct distrib?
    if rand == 0:
        return "F"
    else:
        return "M"


# Appends the generated agent to the agents array.
def generate_agent(agents, fam_id, age, sex):
    agent = {}
    agent["famID"] = fam_id
    agent["age"] = age
    agent["sex"] = sex

    agents.append(agent)
