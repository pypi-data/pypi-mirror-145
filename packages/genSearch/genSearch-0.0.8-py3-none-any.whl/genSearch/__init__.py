## @mainpage Primitive Genetic Algorithm
#
# @section intro_sec Overview
#
# This is a package definining a simple genetic algorithm. This algorithm finds optimum solutions to a problem by modeling evolutionary competition. Users establish a solution's 
# fitness via a `cost` function; the function maps inputs to real numbers based on user criteria. Users give a `decoder` function
# to establish an isomorphism between solutions and bit-strings. The algorithm generates a population of random solutions (as bit-strings), and 
# evaluates their individual fitnesses. Best solutions are selected via tournaments to generate a new population via processes analogous
# to sexual reproduction. This process is iterated a given number of times and the final best solution is returned. 
# \n
# \n
# This particular algorithm is primitive as it treats objects as  binary-strings; other genetic algorithms may abstract objects to more
# complex data structures. 
#

from genSearch.algorithms import *
from genSearch.interface import *
from genSearch.constants import *