'''
    Este é um programa do algoritmo genético de Holland
    para encontrar uma solução para o problema do caixeiro viajante
    * a população é formada por 5 cromossomo 
    * o cromossomo é um vetor binário de 10 posições 
    * cruzamento de um ponto de corte e probabilidade de cruzamento maior que 60
    * mutação por complemento com probabilidade de mutação maior que 90
    * inversão com probabilidade de inversão de 90
    * seleção e substituição elitista 
'''

import itertools
from os import popen   # to concatenate lists
import numpy as np  # to use arrays more easily

POPULATION_SIZE = 10
CHROMOSOME_SIZE = 10
CUT_NUMBER = 5        # number of selected chromosomes to produce offspring
CROSSOVER_RATE = 0.4
MUTATION_RATE = 0.1
INVERTION_RATE = 0.1
MATRIX = np.array([[0, 1, 2, 3, 4],
                   [1, 0, 1, 2, 3],
                   [2, 1, 0, 1, 2],
                   [3, 2, 1, 0, 1],
                   [4, 3, 2, 1, 0]])


# generates a random population of chromosomes
def generate_population(populationSize=POPULATION_SIZE, chromosomeSize=CHROMOSOME_SIZE):
    population = []
    while len(population) < populationSize:
        chromosome = np.random.randint(0,2,(chromosomeSize,))
        while isMonster(chromosome):
            chromosome = np.random.randint(0,2,(chromosomeSize,))
        population.append(chromosome)
    return population

# generates array of chromosome adaptations
def generate_scores(populationSize=POPULATION_SIZE):
    return np.zeros((populationSize,), int)

# displays the population and their respective adaptations
def show_population(population, adaptation_score):
    i = 0
    for chromosome in population:
        print('{:>2} -> {} = {}'.format(i+1, chromosome, adaptation_score[i]))
        i += 1

# calculates the adaptation of a chromosome
def adaptation(chromosome):
    matrixMap = np.array([[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [
                         1, 3], [1, 4], [2, 3], [2, 4], [3, 4]])
    adaptation = 0
    i = 0
    for j in chromosome:
        if j == 1:
            row = matrixMap[i,0]
            column = matrixMap[i,1]
            adaptation += MATRIX[row, column]
        i += 1
    return adaptation * -1


# calculates the adaptation of the chromosomes of a population
def set_adaptation_score(population, adaptation_score):
    i = 0
    for chromosome in population:
        adaptation_score[i] = adaptation(chromosome)
        i += 1


# sort chromosomes based on adaptation array
def sort_population(population, adaptation_score):
    populationSize = len(population)
    i = 0
    for i in range(populationSize - 1):
        for j in range(i+1, populationSize):
            if adaptation_score[j] < adaptation_score[i]:
                # It changes adaptation_scores
                aux = adaptation_score[j]
                adaptation_score[j] = adaptation_score[i]
                adaptation_score[i] = aux

                # It changes the Chromosomes
                aux = population[i]
                population[i] = population[j]
                population[j] = aux

# crossover operation. Crosses the 'cutNumber' most adapted chromosomes
def crossover(population, cutNumber=CUT_NUMBER, crossoverRate=CROSSOVER_RATE, attempts=2):
    descendants = []
    for i in range(cutNumber-1):
        for j in range(i+1, cutNumber):
            if np.random.random() <= crossoverRate:
                print('Entrou | {} <-> {}'.format(i, j))
                cut = np.random.randint(0, CHROMOSOME_SIZE)

                desc1 = list(itertools.chain(
                    population[i][:cut], population[j][cut:]))
                desc2 = list(itertools.chain(
                    population[j][:cut], population[i][cut:]))
                
                count = 0
                while isMonster(desc1) or isMonster(desc2):
                    count += 1
                    cut = np.random.randint(0, CHROMOSOME_SIZE)
                    desc1 = list(itertools.chain(population[i][:cut], population[j][cut:]))
                    desc2 = list(itertools.chain(population[j][:cut], population[i][cut:]))
                    
                    if count >= attempts:
                        break
                
                print(desc1)
                print(desc2)

                if not isMonster(desc1):
                    descendants.append(desc1)
                
                if not isMonster(desc2):
                    descendants.append(desc2)

    return descendants

# mutation operation
def mutation(population, cutNumber=CUT_NUMBER, mutationRate=MUTATION_RATE):
    descendants = []
    for i in range(cutNumber):
        if np.random.random() <= mutationRate:
            print(f'mutation on {i+1}o chromosome!')
            descendant = population[i].copy()
            for j in range(8):
                if np.random.randint(2) == 1:
                    print(f'mutation in gen[{j}]')
                    if descendant[j] == 0:
                        descendant[j] = 1
                    else:
                        descendant[j] = 0
            if not isMonster(descendant):
                descendants.append(descendant)
    return descendants

# inversion operation
def inversion(population, cutNumber=CUT_NUMBER, invertionRate=INVERTION_RATE):
    descendants = []
    for n in range(cutNumber):
        if np.random.random() <= invertionRate:
            print(population[n])
            print(f'Inverteu no {n+1}o cromossomo!')
            descendant = population[n].copy()

            p1 = np.random.randint(0, CHROMOSOME_SIZE-1)
            p2 = np.random.randint(p1+1, CHROMOSOME_SIZE)

            print(f'pivos: {p1} e {p2}')
            descendant = list(itertools.chain(descendant[:p1], reversed(
                descendant[p1:p2+1]), descendant[p2+1:]))
            
            if not isMonster(descendant):
                descendants.append(descendant)
    return descendants

# checks if the chromosome is monster
def isMonster(chromosome):
    edgeA = (1 not in chromosome[:4]) or ((1 in chromosome[:4]) and (doubleEdgeExists(chromosome[:4])))
    edgeB = (1 not in chromosome[4:7]) or ((1 in chromosome[4:7]) and (doubleEdgeExists(chromosome[4:7])))
    edgeC = (1 not in chromosome[7:9]) or ((1 in chromosome[7:9]) and (doubleEdgeExists(chromosome[7:9])))
    edgeD = (chromosome[9] == 0)
    #print(chromosome, edgeA, edgeB, edgeC, edgeD)
    return edgeA or edgeB or edgeC or edgeD

# checks for duplicate edges
def doubleEdgeExists(list):
    i = 0
    for bit in list:
        if bit == 1:
            i += 1
    return (i >= 2)



population = generate_population()   # generating the chromosome population
adaptation_score = generate_scores() # generating array of scores

set_adaptation_score(population, adaptation_score) # calculating the population scores
print('-------------- Population -----------------')
show_population(population, adaptation_score)

sort_population(population, adaptation_score) # sorting the chromossomes based on their adaptation
print('-------------- Sorted Population -----------------')
show_population(population, adaptation_score)

minimum_distance = 999999
count = 0

while adaptation_score[0] != -10:                              # stop condition
    crossovers = np.array(crossover(population)) # crossover
    print('-------------- Crossover -----------------')
    print(crossovers)

    mutants = np.array(mutation(population))     # mutation
    print('-------------- Mutation ------------------')
    print(mutants)

    inverteds = np.array(inversion(population))  # inversion
    print('-------------- Invertion -----------------')
    print(inverteds)

    # mergin all the offspring
    descendants = list(itertools.chain(crossovers, mutants, inverteds))
    descendants_adaptation_score = generate_scores(len(descendants))
    set_adaptation_score(descendants, descendants_adaptation_score)
    sort_population(descendants, descendants_adaptation_score)
    print('-------------- All the Offspring -----------------')
    show_population(descendants, descendants_adaptation_score)

    # mergin offspring and original population
    population = list(itertools.chain(population, descendants))
    adaptation_score = generate_scores(len(population))
    set_adaptation_score(population, adaptation_score)
    sort_population(population, adaptation_score)
    print('-------------- Original Population + Offspring -----------------')
    show_population(population, adaptation_score)

    # selecting the new generation
    population = population[:POPULATION_SIZE]
    print('-------------- New Generation -----------------')
    show_population(population, adaptation_score)
    
    if minimum_distance > adaptation_score[0]:
        minimum_distance = adaptation_score[0]
    
    count += 1
    
print('-------------- Solution -----------------')
print(f'-----> {population[0]} = {adaptation_score[0]} <------')