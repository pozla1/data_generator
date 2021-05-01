import random

import generate_agent
import load


# Generates family member agents with appropriate function calls.
def generate_families(magics_filename, seeds_filename, agents):
    family_seed = random.randint(1, 10000)
    random.seed(family_seed)

    with open(seeds_filename, "a") as seeds:
        seeds.write("Family seed: " + str(family_seed) + "\n")

    magics = load.load_magics(magics_filename)

    fam_id = 0
    # population = 161879       # absolutely temporary so todo
    population = 100  # test
    population_counter = 0

    while population_counter < population:
        rand = random.random()

        if rand < magics["fam_type"][0]:
            # single person family

            # generate 1 single person
            rand = random.random()
            if rand < magics["elderly_num"][0][0]:
                # not elderly single
                generate_agent.generate_single(agents, fam_id, magics)
                population_counter += 1
            else:
                # elderly single
                generate_agent.generate_elderly(agents, fam_id, magics)
                population_counter += 1

        elif rand < magics["fam_type"][0] + magics["fam_type"][1]:
            # family with 1 parent

            # generate 1 parent
            generate_agent.generate_parent(agents, fam_id, magics, parent_type=1, _sex="random")
            population_counter += 1

            # generate children
            rand = random.random()
            if rand < magics["child_num"][1][1]:
                # 1 child
                generate_agent.generate_child(agents, fam_id, magics)
                population_counter += 1
            elif rand < magics["child_num"][1][1] + magics["child_num"][1][2]:
                # 2 children
                for i in range(2):
                    generate_agent.generate_child(agents, fam_id, magics)
                    population_counter += 1
            else:
                # 3+ children
                # todo: 3+ children is always 3 for now...
                for i in range(3):
                    generate_agent.generate_child(agents, fam_id, magics)
                    population_counter += 1

            # generate elders
            rand = random.random()
            if rand < magics["elderly_num"][1][0]:
                # 0 elderly
                pass
            elif rand < magics["elderly_num"][1][0] + magics["elderly_num"][1][1]:
                # 1 elderly
                generate_agent.generate_elderly(agents, fam_id, magics)
                population_counter += 1
            elif rand < magics["elderly_num"][1][0] + magics["elderly_num"][1][1] + magics["elderly_num"][1][2]:
                # 2 elders
                for i in range(2):
                    generate_agent.generate_elderly(agents, fam_id, magics)
                    population_counter += 1
            else:
                # 3+ elders
                # todo: 3+ elders is always 3 for now...
                for i in range(3):
                    generate_agent.generate_elderly(agents, fam_id, magics)
                    population_counter += 1

        elif rand < magics["fam_type"][0] + magics["fam_type"][1] + magics["fam_type"][2]:
            # family with 2 parent

            # generate 2 parents
            generate_agent.generate_parent(agents, fam_id, magics, parent_type=2, _sex="F")  # todo: is it ok?
            population_counter += 1
            generate_agent.generate_parent(agents, fam_id, magics, parent_type=2, _sex="M")
            population_counter += 1

            # generate children
            rand = random.random()
            if rand < magics["child_num"][2][0]:
                # 0 child
                pass
            elif rand < magics["child_num"][2][0] + magics["child_num"][2][1]:
                # 1 child
                generate_agent.generate_child(agents, fam_id, magics)
                population_counter += 1
            elif rand < magics["child_num"][2][0] + magics["child_num"][2][1] + magics["child_num"][2][2]:
                # 2 children
                for i in range(2):
                    generate_agent.generate_child(agents, fam_id, magics)
                    population_counter += 1
            else:
                # 3+ children
                # todo: 3+ children is always 3 for now...
                for i in range(3):
                    generate_agent.generate_child(agents, fam_id, magics)
                    population_counter += 1

            # generate elders
            rand = random.random()
            if rand < magics["elderly_num"][2][0]:
                # 0 elderly
                pass
            elif rand < magics["elderly_num"][2][0] + magics["elderly_num"][2][1]:
                # 1 elderly
                generate_agent.generate_elderly(agents, fam_id, magics)
                population_counter += 1
            elif rand < magics["elderly_num"][2][0] + magics["elderly_num"][2][1] + magics["elderly_num"][2][2]:
                # 2 elders
                for i in range(2):
                    generate_agent.generate_elderly(agents, fam_id, magics)
                    population_counter += 1
            else:
                # 3+ elders
                # todo: 3+ elders is always 3 for now...
                for i in range(3):
                    generate_agent.generate_elderly(agents, fam_id, magics)
                    population_counter += 1

        else:
            # 'other' family type
            # todo: what to do? what does other group mean?
            agent = {}
            agent["famID"] = "OTHER_FAMILY_TYPE"
            agents.append(agent)
            population_counter += 1

        fam_id += 1
