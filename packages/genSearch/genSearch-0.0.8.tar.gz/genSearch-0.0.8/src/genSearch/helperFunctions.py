
'''
Functions used in the genetic search algorithm
'''

import numpy
import genSearch.interface as itf

## Generate Population of n_pop DNA-bitstings of n_len
def population(n_pop, n_len):
    return ["".join([str(s) for s in numpy.random.randint(0, 2, n_len)]) for _ in range(n_pop)]


## Index-match cost scores to population members
def fitness(population):
    return [gcost(c) for c in population]

## Return the fitness score of a DNA-bitstring 
def gcost(indv):
    z = itf.decoder(indv)
    return itf.cost(z)



## Run n_pop tournaments between k randomly selected individuals
def selection(pop, cost, k=3):
    return [tournament(pop, cost, k) for _ in range(len(pop))]

## Simulate a tournament between k individuals 
def tournament(pop, cost, k=3):
    # choose random winner
    v_ix = numpy.random.randint(len(pop))
    # competition
    for ix in numpy.random.randint(0, len(pop)-1, k-1):
        if cost[ix] < cost[v_ix]:
            v_ix = ix
    return pop[v_ix]
    

## Cross-over two DNA-bitstrings  
def crossover(p1, p2, r_cross):
    # define children
    c1, c2 = p1, p2
    # determine if a crossover happens
    if numpy.random.rand() < r_cross:
        # random crossover point
        pt = numpy.random.randint(0, len(c1))
        # crossover
        c1 = p1[:pt] + p2[pt:]
        c1 = p1[pt:] + p2[:pt]
    return c1, c2


## Mutate a DNA-bitstring
def mutate(indv, r_mut):
    f_indv = ""
    for i in range(len(indv)):
        if numpy.random.rand() < r_mut:
            f_indv += str((int(indv[i]) + 1) % 2)
        else:
            f_indv += indv[i]
    return f_indv 


## Return best solution and its cost
def best(pop, cost):
    lo_cost = min(cost)
    lo_ix = cost.index(lo_cost)
    return [itf.decoder(pop[lo_ix]), lo_cost]


