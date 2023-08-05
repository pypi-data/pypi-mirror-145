'''
These are the default hyperparameters for the algorithm. They're stored in a separate namespace for users who prefer to use default values
'''
## Population size
N_POP = 100  
## Bitstring length      
N_LEN = 64         
## Crossover rate     
R_CROSS = 0.5    
## Bit mutation rate       
R_MUT = 1.0 / N_LEN
## Number of generations      
N_GEN = 100             


# Getters (return float)

## Get population
def getPop():
    return N_POP
## Get bitsting length
def getLen():
    return N_LEN
## Get crossover rate
def getCross():
    return R_CROSS
## Get mutation rate
def getMut(): 
    return R_MUT
## Get number of generations
def getGen():
    return N_GEN



# Setters (return bool)

## Set population
def setPop(x):
    N_POP = x
    return True
## Set bitstring length
def setLen(x):
    N_LEN = x
    return True
## Set crossover rate
def setCross(x):
    R_CROSS = x
    return True
## Set mutation rate
def setMut(x):
    R_MUT = x
    return True
## Set number of generations
def setGen(x):
    N_GEN = x
    return True



