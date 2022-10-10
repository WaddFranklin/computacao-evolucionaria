from copy import copy
import numpy as np
import itertools


class Chromossome:

    SIZE = 8

    def __init__(self, chromossome: list = None, lifeTime: int = 0) -> None:
        if chromossome == None:
            self.shape = np.random.randint(0, 2, (self.SIZE,))
            self.adaptation = 0
            self.fitness()
            self.age = 0
            self.lifeTime = lifeTime
        elif len(chromossome) == self.SIZE:
            self.shape = np.array(chromossome)
            self.adaptation = 0
            self.fitness()
            self.age = 0
            self.lifeTime = lifeTime
        else:
            print(f'Chromossome\'s lenght is not compatible!')
            exit()

    def __str__(self) -> str:
        chromossome_string = '['
        for i in self.shape:
            chromossome_string += str(i) + ' '
        chromossome_string += ']'

        return chromossome_string.replace(' ]', ']') + f' -> {self.adaptation} | age: {self.age}/{self.lifeTime}'

    def fitness(self) -> None:
        self.adaptation = 0
        for i in range(self.SIZE - 1):
            if self.shape[i] == 0 and self.shape[i+1] == 1:
                self.adaptation += 1
                i += 2

    def addAge(self):
        self.age += 1


class Population:

    SIZE = 10
    OFFSET = 5            # n | n < SIZE
    EVOLUTION_RATE = 1    # 0 - 10
    CROSSOVER_RATE = 0.4  # 0 - 1
    MUTATION_RATE = 0.1   # 0 - 1
    INVERTION_RATE = 0.1  # 0 - 1
    ROULETTE_SIZE = 10

    def __init__(self) -> None:
        self.chromossomes = self.generate()
        self.offspring = []
        self.minLifeTime = 999999
        self.minAdaptation = 999999
        self.maxAdaptation = -999999
        self.setMinLifeTime()
        self.setMinAdaptation()
        self.setMaxAdaptation()

    def __str__(self) -> str:
        population_string = f'--- Population ----------------------\n'
        count = 1
        for chromossome in self.chromossomes:
            population_string += f'{count} - ' + str(chromossome) + '\n'
            count += 1

        population_string += f'minLifeTime: {self.minLifeTime}\n'
        population_string += f'minAdaptation: {self.minAdaptation}\n'
        population_string += f'maxAdaptation: {self.maxAdaptation}\n'

        return population_string

    def generate(self) -> list:
        chromossomes = []
        for _ in range(self.SIZE):
            lifeTime = np.random.randint(1, 5)
            chromossomes.append(Chromossome(lifeTime=lifeTime))

        return chromossomes

    def setMinLifeTime(self) -> None:
        for chromossome in self.chromossomes:
            if chromossome.lifeTime < self.minLifeTime:
                self.minLifeTime = chromossome.lifeTime

    def setMinAdaptation(self) -> None:
        for chromossome in self.chromossomes:
            if chromossome.adaptation < self.minAdaptation:
                self.minAdaptation = chromossome.adaptation

    def setMaxAdaptation(self) -> None:
        for chromossome in self.chromossomes:
            if chromossome.adaptation > self.maxAdaptation:
                self.maxAdaptation = chromossome.adaptation

    def updateHyperParameters(self):
        self.setMinLifeTime()
        self.setMinAdaptation()
        self.setMaxAdaptation()

    def sort(self, order='desc') -> None:
        i = 0
        for i in range(len(self.chromossomes) - 1):
            for j in range(i+1, len(self.chromossomes)):
                if order == 'desc':
                    if self.chromossomes[j].adaptation > self.chromossomes[i].adaptation:
                        self.swap(i, j)
                elif order == 'asc':
                    if self.chromossomes[j].adaptation < self.chromossomes[i].adaptation:
                        self.swap(i, j)

    def swap(self, i: int, j: int) -> None:
        aux = self.chromossomes[i]
        self.chromossomes[i] = self.chromossomes[j]
        self.chromossomes[j] = aux

    def crossover(self) -> None:
        for i in range(self.OFFSET - 1):
            for j in range(i + 1, self.OFFSET):
                if np.random.random() <= self.CROSSOVER_RATE:
                    print('Entrou | {} <-> {}'.format(i+1, j+1))
                    cut = np.random.randint(0, Chromossome.SIZE)

                    desc1 = list(itertools.chain(
                        self.chromossomes[i].shape[:cut], self.chromossomes[j].shape[cut:]))
                    desc2 = list(itertools.chain(
                        self.chromossomes[j].shape[:cut], self.chromossomes[i].shape[cut:]))

                    chromossome1 = Chromossome(desc1)
                    chromossome2 = Chromossome(desc2)
                    chromossome1.lifeTime = self.calculateLifeTime(
                        chromossome1.adaptation)
                    chromossome2.lifeTime = self.calculateLifeTime(
                        chromossome2.adaptation)
                    
                    print(chromossome1)
                    print(chromossome2)

                    self.offspring.append(chromossome1)
                    self.offspring.append(chromossome2)

    def mutation(self) -> None:
        for i in range(self.OFFSET):
            if np.random.random() <= self.MUTATION_RATE:
                print(f'mutation on {i+1}o chromosome!')
                descendant = self.chromossomes[i].shape.copy()
                for j in range(Chromossome.SIZE):
                    if np.random.randint(2) == 1:
                        print(f'mutation in gen[{j}]')
                        if descendant[j] == 0:
                            descendant[j] = 1
                        else:
                            descendant[j] = 0

                chromossome = Chromossome(list(descendant))
                chromossome.lifeTime = self.calculateLifeTime(
                    chromossome.adaptation)

                self.offspring.append(chromossome)

    def inversion(self) -> None:
        for n in range(self.OFFSET):
            if np.random.random() <= self.INVERTION_RATE:
                print(self.chromossomes[n])
                print(f'Inverteu no {n+1}o cromossomo!')
                descendant = self.chromossomes[n].shape.copy()

                p1 = np.random.randint(0, Chromossome.SIZE - 1)
                p2 = np.random.randint(p1 + 1, Chromossome.SIZE)

                print(f'pivos: {p1} e {p2}')
                descendant = list(itertools.chain(descendant[:p1], reversed(
                    descendant[p1:p2+1]), descendant[p2+1:]))

                chromossome = Chromossome(descendant)
                chromossome.lifeTime = self.calculateLifeTime(
                    chromossome.adaptation)
                
                print(f'descendant -> ' + str(chromossome))

                self.offspring.append(chromossome)

    def calculateLifeTime(self, adaptation: int) -> int:
        return int(self.minLifeTime + 2*self.EVOLUTION_RATE*((adaptation - self.minAdaptation)/(self.maxAdaptation - self.minAdaptation)))

    def showOffspring(self) -> None:
        count = 1
        print(f'--- Offspring ----------------------')
        for chromossome in self.offspring:
            print(f'{count} - ' + str(chromossome))
            count += 1

    def isEmpty(self, ChromossomeList) -> bool:
        return len(ChromossomeList) == 0

    def merge(self) -> None:
        print(f'--- Merging ...')
        while not self.isEmpty(self.offspring):
            self.chromossomes.append(self.offspring.pop())

    def selection(self, selectionMode: str) -> None:
        if selectionMode == 'elitism':
            self.elitism()
        elif selectionMode == 'tournament':
            self.tournament()
        elif selectionMode == 'roullete':
            self.roulette()
        elif selectionMode == 'lifetime':
            self.lifeTime()
        else:
            print(f'Invalid selection mode!')
            exit()

    def elitism(self) -> None:
        self.merge()
        self.sort()
        while len(self.chromossomes) > self.SIZE:
            self.chromossomes.pop()

    def tournament(self) -> None:
        competitors = []
        champions = []
        self.merge()
        while len(champions) < self.SIZE:
            competitors = self.convocation()
            champions.append(self.getChampion(competitors))
        self.chromossomes.clear()
        self.chromossomes = champions

    def convocation(self) -> list:
        called = []
        while len(called) < self.OFFSET:
            index = np.random.randint(len(self.chromossomes))
            called.append(copy(self.chromossomes[index]))

        return called

    def getChampion(self, called: list) -> Chromossome:
        index = -1
        adaptation = -999999
        for i in range(len(called)):
            if called[i].adaptation > adaptation:
                index = i
                adaptation = called[i].adaptation

        return called[index]

    def roulette(self) -> None:
        self.merge()
        self.sort()
        roulette = self.buildRoulette()
        self.chromossomes.clear()
        self.chromossomes = self.sortition(roulette)

    def getTotalAdaptation(self, preSelecteds: list) -> int:
        totalAdaptation = 0
        for chromossome in preSelecteds:
            totalAdaptation += chromossome.adaptation

        return totalAdaptation

    def buildRoulette(self) -> list:
        roulette = []
        preSelecteds = copy(self.chromossomes[:self.OFFSET])
        totalAdaptation = self.getTotalAdaptation(preSelecteds)

        for chromossome in preSelecteds:
            sizeInRoulette = int(
                (chromossome.adaptation * self.ROULETTE_SIZE) / totalAdaptation)
            for _ in range(sizeInRoulette):
                if len(roulette) < self.ROULETTE_SIZE:
                    roulette.append(chromossome)

        return roulette

    def sortition(self, roulette: list) -> list:
        drawn = []
        while len(drawn) < self.SIZE:
            index = np.random.randint(0, len(roulette))
            drawn.append(copy(roulette[index]))

        return drawn

    def lifeTime(self):
        self.merge()
        self.addAgeAll()
        self.deathByAge()
        self.updateHyperParameters()
        self.sort()

    def addAgeAll(self) -> None:
        for chromossome in self.chromossomes:
            chromossome.addAge()

    def deathByAge(self):
        for chromossome in self.chromossomes:
            #print(f'atual -> ' + str(chromossome))
            if chromossome.age > chromossome.lifeTime:
                #print(f'matando -> ' + str(chromossome))
                self.chromossomes.remove(chromossome)

    def stopCondition(self):
        return self.chromossomes[0].adaptation == 4

    def run(self, selectionMode: str = 'elitism') -> None:
        while not self.stopCondition():
            self.sort()
            self.crossover()
            self.mutation()
            self.inversion()
            self.selection(selectionMode)

        print(f'Problem\'s solution: ' + str(self.chromossomes[0]))


p = Population()
p.run(selectionMode='lifetime')