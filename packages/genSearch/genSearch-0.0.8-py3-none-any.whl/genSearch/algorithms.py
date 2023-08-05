from genSearch.helperFunctions import *
import genSearch.interface as itf



##
#
# @section intro_sec Overview
# This is the genetic algorithm. Users establish a bijection between bistrings and objects in `decoder`. Users establish a map from objects to real
# numbers in `cost`. The algorithm then runs and returns an approximation of the minimum of `cost`: the algorithm generates a pseudorandom population
# of bitstrings. It ranks them according to their corresponding object's cost. It selects a new population from these by running tournaments. These are 
# then crossed over. The offspring are then mutated. This process is iterated on the new population a given amount of times. When the iterations end, 
# the algorithm returns the fittest from the final generation
#
# @param Decoder: f: str -> <E>, internal binary strings to client-side solutions objects
# @param Cost: f: <E> -> Double,  client-side solution objects to real numbers
# @param n_pop Size of population
# @param n_len Length of bitstring
# @param r_cross Probability of crossover during reproduction stage
# @param r_mut Probability of a bit swapping during mutation stage
# @param n_gen Number of generations or iterations
# 
# @return solution: <E> type object
def genetic_simulation(decoder, cost):
    
    # configure interface
    itf.cost = cost
    itf.decoder = decoder
    
    # initialize population
    pop = population(cts.N_POP, cts.N_LEN)
    # iterate generations
    for gen in range(cts.N_GEN):
        # assign fitness scores
        fit = fitness(pop)
        sol = best(pop, fit)
        # select reproducing individuals
        vic = selection(pop, fit)
        # initialize next generation
        nxt_pop = []
        # reproduce
        for ps in range(0, cts.N_POP, 2):
            c1, c2 = crossover(vic[ps], vic[ps+1], cts.R_CROSS)
            c1, c2 = mutate(c1, cts.R_MUT), mutate(c2, cts.R_MUT)
            nxt_pop.append(c1)
            nxt_pop.append(c2)
        # update population
        pop = nxt_pop
    return sol