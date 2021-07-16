# -----------------------------------------------------------
# simple-ga-tcp.py
# 
# This code is the implementation of Test Case Prioritization
# using Genetic Algorithm. The algorithm was proposed by Habtemariam
# and Mohapatra with paper title "A Genetic Algorithm-Based Approach
# for Test Case Prioritization"
#
# (C) 2021 Evan Lokajaya & Zara Veda, Bandung, Indonesia
# email zaraveda.zv@gmail.com
# -----------------------------------------------------------

def prio_ga(t, tr, max_gen, p_c, p_m):
    """
    Perform prioritization

    Parameters:

    t: set of test case
    tr: test fault detection details as traceability matrix
    max_gen: maximum generation
    p_c: crossover probability
    p_m: mutation probability

    return: res_min; the sequence of minimized test case with maximum faults
    """

    print("processing GA prioritization..")

    p = []
    l = 2           # length of chromosome
    pop_size = 20

    while True:
        initial_population(pop_size, l)
        g = 1

        while True:
            calculate_fitness(p, tr)
            crossover(p_c, p, l)
            mutation(p_m, p, l)

            if find_full_fault(l, tr):
                res_min = find_max(p)
            else:
                g = g + 1

            if g <= max_gen:
                break


        l = l + 1

        if l <= chromolen:
            break

    return res_min

def find_full_fault(len, tr):
    full_fault = [1] * len

    for row in tr:
        if row == full_fault:
            return True
        else:
            return False

def initial_population(pop_size, chromolen):
    """
    Initialize population from test cases

    Parameters:

    pop_size: population size
    chromolen: length of the chromosome

    return: None
    """

    print("initializing population..")
    a = 1

    while True:
        p_a = []         # permutation encoding

        while True:
            rand_tc = random.choice(t)
            p_a = p_a or rand_tc
            if abs(p_a) <= chromolen:
                break
        
        i = i + 1
        if i <= pop_size:
            break

def calculate_fitness(p, tr):
    """
    Calculate fitness value

    Parameters:

    p: 
    tr: 

    return: None
    """

    i = 1
    pop_size = len(p)
    fitness_val = [0] * pop_size
    total_faults = len(tr[0])

    while True:
        # TODO: insert calculate fitness eq.
        # tc = tc with value string of tr
        revealed_faults = 0
        for tc in p[i]:
            # value 1 kromosom (1 p) = array of int; angka test case ke berapa
            revealed_faults = revealed_faults or int(tr[tc])

        fitness_val[i] = revealed_faults / total_faults

        i = i + 1

        if i < pop_size:
            break

def crossover(p_c, p, l):
    """
    Perform crossover at crossover point (cp)

    Parameters:

    p_c: crossover probability
    p:
    l:

    return: None
    """

    print("crossover chromosomes..")

    # TODO: insert loop for p_c percentage of chromosome
    # - generate cp (crossover point)
    # - exchange chromosome at cp
    # - end loop

def mutation(p_m, p, l):
    """
    Perform mutation at mutation point (mp)

    Parameters:

    p_m: mutation probability
    p: population
    l:

    return: None
    """

    print("mutation chromosomes..")
    # TODO: insert loop for pm percentage of chromosome
    # - generate mp (mutation point)
    # - replace duplicate test case with test case which is not
    # present in that chromosome
    # - end loop

def find_max(p):
    """
    Perform sort the population in ascending order of their
    fitness value

    Parameters:

    p: population

    return: p_sorted_asc; population in ascending order by fitness value
    """

    print("sort population in asc order..")
    p_sorted_asc = p.sort()

    return p_sorted_asc

def main():
    """
    Main function

    Variables:

    t: set of test case
    tr: traceability matrix; test case fault detection details
    p_c: crossover probability
    p_m: mutation probability
    max_gen: maximum GA generation
    """

    # TODO: bikin struct buat chromosome

    t = []
    tr = ["" for i in range(3)]
    p_c = 0.0
    p_m = 0.0
    max_gen = 100

    prio_ga(t, tr, max_gen, p_c, p_m)

if __name__ == "__main__":
    main()