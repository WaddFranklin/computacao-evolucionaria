'''
    Este é um programa do algoritmo genético de Holland
    para encontrar o número binário dentre do interválao de 
    [0,255] que apresenta a maior ocorrencia da sub string 01
    * a população é formada por 10 cromossomo 
    * o cromossomo é um vetor binário de 8 posições 
    * cruzamento de um ponto de corte e probabilidade de cruzamento maior que 60
    * mutação por complemento com probabilidade de mutação maior que 90
    * inversão com probabilidade de inversão de 90
    * seleção e substituição elitista 
'''

import itertools   # to concatenate lists
import numpy as np # to use arrays more easily

POPULATION_SIZE = 10
CHROMOSOME_SIZE = 8
CUT_NUMBER = 5       # number of selected chromosomes to produce offspring
CROSSOVER_RATE = 0.4
MUTATION_RATE = 0.1
INVERTION_RATE = 0.1

# generates a random population of chromosomes
def generate_population(populationSize=POPULATION_SIZE, chromosomeSize=CHROMOSOME_SIZE):
    return np.random.randint(0, 2, (populationSize, chromosomeSize))

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
    adaptation = 0
    for i in range(CHROMOSOME_SIZE - 1):
        if chromosome[i] == 0 and chromosome[i+1] == 1:
            adaptation += 1
            i += 2
    return adaptation

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
            if adaptation_score[j] > adaptation_score[i]:
                # It changes adaptation_scores
                aux = adaptation_score[j]
                adaptation_score[j] = adaptation_score[i]
                adaptation_score[i] = aux

                # It changes the Chromosomes
                aux = population[i]
                population[i] = population[j]
                population[j] = aux

# crossover operation. Crosses the 'cutNumber' most adapted chromosomes
def crossover(population, cutNumber=CUT_NUMBER, crossoverRate=CROSSOVER_RATE):
    descendants = []
    for i in range(cutNumber-1):
        for j in range(i+1, cutNumber):
            if np.random.random() <= crossoverRate:
                print('Entrou | {} <-> {}'.format(i,j))
                cut = np.random.randint(0, CHROMOSOME_SIZE)
                
                desc1 = list(itertools.chain(population[i][:cut], population[j][cut:]))
                desc2 = list(itertools.chain(population[j][:cut], population[i][cut:]))
                
                print(desc1)
                print(desc2)
                
                descendants.append(desc1)
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
            descendants.append(descendant)
    return descendants
                
# inversion operation
def inversion(population, cutNumber=CUT_NUMBER, invertionRate=INVERTION_RATE):
    descendants = []
    for n in range(CUT_NUMBER):
        if np.random.random() <= INVERTION_RATE:
            print(population[n])
            print(f'Inverteu no {n+1}o cromossomo!')
            descendant = population[n].copy()
            
            p1 = np.random.randint(0,CHROMOSOME_SIZE-1)
            p2 = np.random.randint(p1+1,CHROMOSOME_SIZE)
            
            print(f'pivos: {p1} e {p2}')
            descendant = list(itertools.chain(descendant[:p1], reversed(descendant[p1:p2+1]), descendant[p2+1:]))
            descendants.append(descendant)
    return descendants
            

population = generate_population()   # generating the chromosome population
adaptation_score = generate_scores() # generating array of scores

set_adaptation_score(population, adaptation_score) # calculating the population scores
print('-------------- Population -----------------')
show_population(population, adaptation_score)

sort_population(population, adaptation_score) # sorting the chromossomes based on their adaptation
print('-------------- Sorted Population -----------------')
show_population(population, adaptation_score)

while adaptation_score[0] != 4:                  # stop condition
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
