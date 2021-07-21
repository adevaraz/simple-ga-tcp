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
from numpy.core.numeric import full

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
    chromolen = len(t)
    pop_size = 20
    res_min = []
    ts_fault = np.array([])

    while True:
        p = np.array(initial_population(t, pop_size, l))
        g = 1       # generation number

        print("=====================================")
        print("TCP with Genetic Algorithm")
        print("=====================================")
        print("generation:", g)
        while True:
            print("population:")
            print(p)

            print("-------------------------------------")

            fitness_val = calculate_fitness(p, tr)
            print("fitness value")
            print(fitness_val)

            p = crossover(p_c, p, l)
            print("crossover result:")
            print(p)
            print("-------------------------------------")

            p = mutation(t, p_m, p, l)
            print("mutation result:")
            print(p)
            print("-------------------------------------")

            ts_fault = generate_binary_fault(p, tr)
            fitness_val = calculate_fitness(p, tr)

            print("population   ", "fitness value")
            i = 0
            for i in range(len(p)):
                print(p[i], fitness_val[i])
            print("-------------------------------------")

            fault_percentage = 1.0
            found = False
            while not found:
                if find_full_fault(ts_fault, fault_percentage):
                    res_min = find_max(p, fitness_val)
                    found = True
                else:
                    fault_percentage = fault_percentage - 0.05

                if fault_percentage <= 0.0:
                    break
        
            if found:
                break
            else:
                g = g + 1

            if g > max_gen:
                break


        l = l + 1

        if l > chromolen:
            break

    return res_min

def find_full_fault(ts_fault, fault_percentage):
    full_fault = int(len(ts_fault[0]) * fault_percentage)

    for row in ts_fault:
        if row.count('1') == full_fault:
            return True
        else:
            return False

def generate_binary_fault(p, tr):

    i = 0
    pop_size = len(p)
    total_faults = len(tr[0][1])
    result = np.array([''.join('0' for _ in range(total_faults))] * len(p))
    while True:
        fault_ba = bitarray(result[i])

        for tc in p[i]:
            tc_fault = [item for item in tr if item[0] == tc] # search for tc fault
            fault_ba = fault_ba | bitarray(tc_fault[0][1]) # or operator

        result[i] = fault_ba.to01() # get string back

        i = i + 1

        if i >= pop_size:
            break

    return result

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
    total_faults = len(tr[0][1])

    while True:
        fault = ''.join('0' for _ in range(total_faults))
        fault_ba = bitarray(fault)
        for tc in p[i]:
            tc_fault = [item for item in tr if item[0] == tc] # search for tc fault
            fault_ba = fault_ba | bitarray(tc_fault[0][1]) # or operator

        fault = fault_ba.to01() # get string back
        fitness_val[i] = fault.count('1') / total_faults

        i = i + 1

        if i >= pop_size:
            break

    return np.array(fitness_val)

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

    # i = int(len(p) / 2)
    i = 0
    count = 0
    while count <= num_of_mutation and i < len(p):
        mp = random.randrange(1, l)

        duplicate_index = find_duplicate(p[i])
        if duplicate_index != None:
            while True:
                choosen = random.choice(t)

                if choosen not in p[i]:
                    p[i][duplicate_index] = choosen
                    break

        i += 1
        count += 1
    
    return p

def find_duplicate(chromosome):
    set_of_gen = set()

    for i, gen in enumerate(chromosome):
        if gen in set_of_gen:
            return i
        else:
            set_of_gen.add(gen)

def find_max(p, fitness):
    """
    Perform sort the population in ascending order of their
    fitness value

    Parameters:

    p: population

    return: p_sorted_asc; population in ascending order by fitness value
    """

    print("sort population in asc order by fitness value..")
    # TODO: ganti cara sort pake numpy
    p_sorted_asc = [p for _, p in sorted(zip(fitness.tolist(), p.tolist()))]
    sorted_fitness = sorted(fitness.tolist())
    result = [p_sorted_asc[len(p_sorted_asc) - 1], sorted_fitness[len(sorted_fitness) - 1]]

    print(np.array(p_sorted_asc))
    print("-------------------------------------")

    return result

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

    t = np.array([1, 2, 3, 4, 5, 6]) # tc is represented in number
    tr = [(1, '101010'),
          (2, '110100'),
          (3, '001101'),
          (4, '101000'),
          (5, '000001'),
          (6, '000000')]
    p_c = 0.6
    p_m = 0.4
    # use three condition of number of generation: 25, 55, and 70
    max_gen = 25
    # max_gen = 55
    # max_gen = 70

    res = prio_ga(t, tr, max_gen, p_c, p_m)
    print("\n=====================================")
    print("best chromosom is:", res)
    print("=====================================")


if __name__ == "__main__":
    main()