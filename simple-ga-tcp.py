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

import itertools
import random
import numpy as np
from bitarray import bitarray

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
    pop_size = 100

    while True:
        p = initial_population(pop_size, l)
        g = 1       # generation number

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

def initial_population(t, pop_size, chromolen):
    """
    Initialize population from test cases

    Parameters:

    pop_size: population size
    chromolen: length of the chromosome

    return: None
    """

    print("initializing population..")

    permutation_res = list(itertools.permutations(t, chromolen))
    p = get_rand_elms(permutation_res, pop_size)

    return p

def get_rand_elms(arr, max_elm):
    rand_elms = []
    i = 0

    while i < max_elm:
        choosen = random.choice(arr)

        if choosen not in rand_elms:
            rand_elms.append(choosen)
            i += 1

    return rand_elms

def calculate_fitness(p, tr):
    """
    Calculate fitness value

    Parameters:

    p: 
    tr: 

    return: None
    """

    i = 0
    pop_size = len(p)
    fitness_val = [0] * pop_size
    total_faults = len(tr[0])

    while True:
        fault = ''.join('0' for _ in range(total_faults))
        fault_ba = bitarray(fault)
        for tc in p[i]:
            fault_ba = fault_ba | bitarray(tr[tc-1]) # or operator

        fault = fault_ba.to01() # get string back
        fitness_val[i] = fault.count('1') / total_faults

        i = i + 1

        if i >= pop_size:
            break

    return fitness_val

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

    num_of_crossover = p_c * len(p)

    i = 0
    while i <= num_of_crossover:
        cp = random.randrange(1, l)

        p1_f = p[i][:cp]
        p1_b = p[i][cp:]

        p2_f = p[i+1][:cp]
        p2_b = p[i+1][cp:]

        child1 = np.concatenate((p1_f, p2_b))
        child2 = np.concatenate((p2_f, p1_b))

        p = np.vstack((p, child1, child2))

        i += 2

    return p

def mutation(t, p_m, p, l):
    """
    Perform mutation at mutation point (mp)

    Parameters:

    p_m: mutation probability
    p: population
    l:

    return: None
    """

    print("mutating chromosomes..")

    num_of_mutation = p_m * len(p)

    i = len(p) / 2
    while i <= num_of_mutation:
        mp = random.randrange(1, l)

        duplicate_index = find_duplicate(p[i])
        if duplicate_index != None:
            while True:
                choosen = random.choice(t)

                if choosen not in p[i]:
                    p[i][duplicate_index] = choosen
                    break

        i += 1
    
    return p

def find_duplicate(chromosome):
    set_of_gen = set()

    for i, gen in enumerate(chromosome):
        if gen in set_of_gen:
            return i
        else:
            set_of_gen.add(gen)

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
    # TODO: modify tr to tuple

    t = np.array(['t1', 't2', 't3', 't4'])
    tr = ["" for i in range(3)]
    p_c = 0.6
    p_m = 0.4
    # use three condition of number of generation: 25, 55, and 70
    max_gen = 25

    # prio_ga(t, tr, max_gen, p_c, p_m)

    p = np.asarray(initial_population(t, 4, 3))
    print("population:")
    print(p)

    p = crossover(p_c, p, 3)
    print(p)

    mutated_pop = mutation(t, p_m, p, 3)
    print("mutated population:")
    print(mutated_pop)

if __name__ == "__main__":
    main()