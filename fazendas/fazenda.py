import numpy as np

'''
    custo ->  n * (lucro - agua * preco)
'''

farms = {
    0: {'cultivated': 40, 'avaliable': 180},
    1: {'cultivated': 65, 'avaliable': 220},
    2: {'cultivated': 35, 'avaliable': 95}
}

cultivation = {
    0: {'name': 'corn', 'cultivated': 66, 'water': 5.5, 'profit': 500},
    1: {'name': 'rice', 'cultivated': 88, 'water': 4, 'profit': 400},
    2: {'name': 'bean', 'cultivated': 40, 'water': 3.5, 'profit': 180}
}


class Chromosome:
    
    CHROMOSSOME_DIMENSION = {'rows': 3, 'cols': 3}

    def __init__(self, shape: list = []) -> None:
        if len(shape) == 0:
            self.shape = np.random.randint(0, 2, (self.CHROMOSSOME_DIMENSION['rows'], self.CHROMOSSOME_DIMENSION['cols']))
        else:
            self.shape = np.array(shape)
        self.adaptation = self.fitness()
        
    def __str__(self) -> str:
        return f'{str(self.shape)} -> adaptation: {self.adaptation}'

    def fitness(self) -> float:
        totalCost = 0
        for i in range(3):
            totalCost += self.cost(self.shape[i])
        return totalCost

    def cost(self, farm: list, waterPrice: float = 1.0) -> float:
        totalFarmCost = 0
        for i in range(3):
            totalFarmCost += (farm[i] * (cultivation[i]['profit'] -
                                         cultivation[i]['water'] * waterPrice))
        return totalFarmCost


class Population:

    POPULATION_SIZE = 10
    MAX_AGES = 100000
    OFFSET = 5
    CROSSOVER_RATE = 0.5
    MUTATION_RATE = 0.75
    INVERTION_RATE = 0.75

    def __init__(self) -> None:
        self.chromosomes = self.generate()
        self.offspring = []
        self.age = 0

    def __str__(self) -> str:
        string = ''
        for chromosome in self.chromosomes:
            string += f'{str(chromosome)}\n'
        string += '#######################\n'
        for chromosome in self.offspring:
            string += f'{str(chromosome)}\n'
        return string

    def generate(self) -> list:
        chromosomes = []
        while len(chromosomes) < self.POPULATION_SIZE:
            chromosome = Chromosome()
            if not self.isMonster(chromosome):
                chromosomes.append(chromosome)
        return chromosomes

    def isMonster(self, chromosome: Chromosome) -> bool:
        for i in range(3):
            # # print(farms[i]['avaliable'])
            if not self.isFarmValid(chromosome.shape[i], farms[i]['avaliable']):
                # # print('is monster')
                return True
        # # print('is not monster')
        return False

    def isFarmValid(self, culture: list, avaliable: int) -> bool:
        cultivated = (culture[0] * cultivation[0]['cultivated'] +
                      culture[1] * cultivation[1]['cultivated'] +
                      culture[2] * cultivation[2]['cultivated'])
        # # print(f'cultivated: {cultivated} | avaliable: {avaliable}')
        return (cultivated < avaliable)
    
    def sort(self, order='desc') -> None:
        i = 0
        for i in range(len(self.chromosomes) - 1):
            for j in range(i+1, len(self.chromosomes)):
                if order == 'desc':
                    if self.chromosomes[j].adaptation > self.chromosomes[i].adaptation:
                        self.swap(i, j)
                elif order == 'asc':
                    if self.chromosomes[j].adaptation < self.chromosomes[i].adaptation:
                        self.swap(i, j)

    def crossover(self) -> None:
        for i in range(self.OFFSET - 1):
            for j in range(i + 1, self.OFFSET):
                if np.random.random() <= self.CROSSOVER_RATE:
                    # print('Entrou | {} <-> {}'.format(i+1, j+1))
                    # cut = np.random.randint(0, Chromosome.CHROMOSSOME_DIMENSION['rows'])

                    desc1 = [self.chromosomes[i].shape[0], self.chromosomes[j].shape[1], self.chromosomes[i].shape[2]]
                    desc2 = [self.chromosomes[j].shape[0], self.chromosomes[i].shape[1], self.chromosomes[j].shape[2]]

                    chromosome1 = Chromosome(desc1)
                    chromosome2 = Chromosome(desc2)
                    
                    # chromosome1.lifeTime = self.calculateLifeTime(chromosome1.adaptation)
                    # chromosome2.lifeTime = self.calculateLifeTime(chromosome2.adaptation)

                    # # print(chromosome1)
                    # # print(chromosome2)

                    if not self.isMonster(chromosome1):
                        self.offspring.append(chromosome1)
                    if not self.isMonster(chromosome2):
                        self.offspring.append(chromosome2)

    def mutation(self) -> None:
        for i in range(self.OFFSET):
            if np.random.random() <= self.MUTATION_RATE:
                # print(f'mutation on {i+1}o chromosome!')
                descendant = self.chromosomes[i].shape.copy()
                # print(descendant)
                
                for row in descendant:
                    for j in range(Chromosome.CHROMOSSOME_DIMENSION['cols']):
                        if np.random.randint(2) == 1:
                            # print(f'mutation in gen[{j}]')
                            row[j] = np.random.randint(6)
                
                # print(descendant)
                chromosome = Chromosome(descendant)
                # chromosome.lifeTime = self.calculateLifeTime(
                #     chromosome.adaptation)
                if not self.isMonster(chromosome):
                    self.offspring.append(chromosome)

    def inversion(self) -> None:
        for n in range(self.OFFSET):
            if np.random.random() <= self.INVERTION_RATE:
                # print(self.chromosomes[n])
                # print(f'Inverteu no {n+1}o cromossomo!')
                descendant = np.transpose(self.chromosomes[n].shape.copy())
                
                chromosome = Chromosome(descendant)
                # chromossome.lifeTime = self.calculateLifeTime(
                #     chromossome.adaptation)

                # print(f'descendant -> ' + str(chromosome))
                
                if not self.isMonster(chromosome):
                    self.offspring.append(chromosome)

    def selection(self, selectionMode: str) -> None:
        if selectionMode == 'elitism':
            self.elitism()
        else:
            # print(f'Invalid selection mode!')
            exit()
            
    def elitism(self) -> None:
        self.merge()
        # print('*************** lista depois do merge *************************************')
        # print(self)
        self.sort()
        # print('+++++++++++++++ lista depois do sort ++++++++++++++++++++++++++++++++++++++')
        # print(self)
        while len(self.chromosomes) > self.POPULATION_SIZE:
            self.chromosomes.pop()
            
    def merge(self) -> None:
        # print(f'--- Merging ...')
        while not self.isEmpty(self.offspring):
            # print('---------- MERGING -------------------------------------')
            self.chromosomes.append(self.offspring.pop())
            
    def isEmpty(self, ChromosomeList) -> bool:
        return len(ChromosomeList) == 0

    def swap(self, i: int, j: int) -> None:
        aux = self.chromosomes[i]
        self.chromosomes[i] = self.chromosomes[j]
        self.chromosomes[j] = aux
        
    def stopCondition(self):
        return self.age > self.MAX_AGES
    
    def incrementAge(self):
        self.age += 1
    
    def run(self, selectionMode: str = 'elitism') -> None:
        while not self.stopCondition():
            self.sort()
            self.crossover()
            self.mutation()
            self.inversion()
            self.selection(selectionMode)
            self.incrementAge()
            times = (self.age / self.MAX_AGES) * 100
            
            print(f'\rAGE: {self.age} [' + '|'*int(times) + ' '*int(100 - times) + ']', end='')
        print(f'\nProblem\'s solution:\n' + str(self.chromosomes[0]))


p = Population()
p.run()