import rw
import random


# Loads and processes data, then assigns educational institutions to the agents.
def add_education(agents, educational_institutions_filename, creches_filename, schools_filename, locality_filter,
                  misc_consts_filename, report_filename):

    # Load the needed data.
    educational_institutions = rw.xls_to_array_of_dicts("!input_files\\" + educational_institutions_filename)
    creches = rw.xls_to_array_of_dicts("!input_files\\" + creches_filename)
    schools = rw.xls_to_array_of_dicts("!input_files\\" + schools_filename)
    misc_consts = rw.load_from_json("!input_files\\" + misc_consts_filename)

    # Process data.
    educational_institutions = filter_by_locality(educational_institutions, locality_filter)
    educational_institutions = join_capacity(educational_institutions, creches, schools)

    # Assign educational institutions to the agents.
    agents = assign_institutions(agents, educational_institutions, misc_consts)

    # Write to report
    rw.append_to_file("!output_files\\" + report_filename, "Education: Educational institutes assigned.\n")

    return agents


# Filters the educational institutions by given locality.
def filter_by_locality(educational_institutions, locality_filter):
    tmp = []
    for institute in educational_institutions:
        if institute["MEGYE"] == locality_filter:
            tmp.append(institute)
    educational_institutions = tmp
    return educational_institutions


# Adds the capacity of the educational_institutions from the other data sources.
def join_capacity(educational_institutions, creches, schools):
    for institute in educational_institutions:
        institute["CAPACITY"] = 0

        if institute["KATEGORIA_NEV"] == "bölcsőde":
            address = institute["IRANYITOSZAM"] + " " + institute["TELEPULES"] + " "\
                      + institute["UTCA"].split(" ", 1)[0]
            for creche in creches:
                if address == creche["Cím"][:len(address)] and creche["Férőhelyek"] != "":
                    institute["CAPACITY"] = int(creche["Férőhelyek"])
        else:
            address = institute["IRANYITOSZAM"] + " " + institute["TELEPULES"] + ", "\
                      + institute["UTCA"].split(" ", 1)[0]
            for school in schools:
                if address == school["Intézmény címe"][:len(address)]:
                    if institute["KATEGORIA_NEV"] == "óvoda":
                        institute["CAPACITY"] += int(school["Óvodások száma"])
                    elif institute["KATEGORIA_NEV"] == "általános iskola":
                        institute["CAPACITY"] += int(school["Általános iskolások száma"])
                    elif institute["KATEGORIA_NEV"] == "gimnázium":
                        institute["CAPACITY"] += int(school["Gimnáziumi tanulok száma"])
                    elif institute["KATEGORIA_NEV"] == "szakközépiskola":
                        institute["CAPACITY"] += int(school["Technikum, szakgimnáziumosok száma"])
                    elif institute["KATEGORIA_NEV"] == "szakiskola":
                        institute["CAPACITY"] += int(school["Szakiskolások, készségfejlesztős diákok száma"])
                    elif institute["KATEGORIA_NEV"] == "fejlesztő iskola":
                        institute["CAPACITY"] += int(school["Fejlesztő nevelés-oktatásban résztvevő tanulók száma"])
                    elif institute["KATEGORIA_NEV"] == "művészeti iskola":
                        institute["CAPACITY"] += int(school["Gimnáziumi tanulok száma"])
                        institute["CAPACITY"] += int(school["Technikum, szakgimnáziumosok száma"])

    return educational_institutions


# Assigns educational institutions to the appropriate agents.
def assign_institutions(agents, educational_institutions, misc_consts):

    # Separate agents by age intervals of school types.
    agents_creche = []
    agents_nursery = []
    agents_primary = []
    agents_secondary = []
    agents_tmp = []

    for agent in agents:
        if misc_consts["education_ages"][0][0] <= agent["age"] <= misc_consts["education_ages"][0][1]:
            agents_creche.append(agent)
        elif misc_consts["education_ages"][1][0] <= agent["age"] <= misc_consts["education_ages"][1][1]:
            agents_nursery.append(agent)
        elif misc_consts["education_ages"][2][0] <= agent["age"] <= misc_consts["education_ages"][2][1]:
            agents_primary.append(agent)
        elif misc_consts["education_ages"][3][0] <= agent["age"] <= misc_consts["education_ages"][3][1]:
            agents_secondary.append(agent)
        else:
            agents_tmp.append(agent)

    agents = agents_tmp

    # Separate educational institutions by age intervals.
    institutions_creche = []
    institutions_nursery = []
    institutions_primary = []
    institutions_secondary = []

    for institute in educational_institutions:
        if institute["CAPACITY"] != 0:
            if institute["KATEGORIA_NEV"] == "bölcsőde":
                institutions_creche.append(institute)
            elif institute["KATEGORIA_NEV"] == "óvoda":
                institutions_nursery.append(institute)
            elif institute["KATEGORIA_NEV"] == "általános iskola":
                institutions_primary.append(institute)
            else:
                institutions_secondary.append(institute)

    # Assign the the separated group of educational institutions to the separated group of agents.
    agents = assign_institute(agents, agents_creche, institutions_creche, "bolcs")
    agents = assign_institute(agents, agents_nursery, institutions_nursery, "ovoda")
    agents = assign_institute(agents, agents_primary, institutions_primary, "altal")
    agents = assign_institute(agents, agents_secondary, institutions_secondary, "GET")

    return agents


# Assigns a separated group of educational institutions to a separated group of agents.
def assign_institute(agents, agents_separated, institutions_separated, institute_type):
    for agent in agents_separated:
        if len(institutions_separated) == 0:
            break
        institute = random.choice(institutions_separated)
        institute["CAPACITY"] -= 1
        if institute["CAPACITY"] == 0:
            institutions_separated.remove(institute)

        if institute_type == "GET":
            if institute["KATEGORIA_NEV"] == "gimnázium":
                institute_type = "gimna"
            elif institute["KATEGORIA_NEV"] == "szakközépiskola":
                institute_type = "szakk"
            elif institute["KATEGORIA_NEV"] == "szakiskola":
                institute_type = "szaki"
            elif institute["KATEGORIA_NEV"] == "fejlesztő iskola":
                institute_type = "fejle"
            elif institute["KATEGORIA_NEV"] == "művészeti iskola":
                institute_type = "muves"

        agent["locations"] = [agent["locations"], {"typeID": 3, "locID": str(int(institute["poi_id"]))
                              + institute_type}]
        agents.append(agent)

    return agents
