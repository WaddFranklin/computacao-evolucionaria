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
    0: {'cultivated': 66, 'water': 5.5, 'profit': 500},
    1: {'cultivated': 88, 'water': 4, 'profit': 400},
    2: {'cultivated': 40, 'water': 3.5, 'profit': 180}
}


class Chromosome:

    def __init__(self) -> None:
        self.shape = np.random.randint(0, 2, (3, 3))
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

    def __init__(self) -> None:
        self.chromosomes = self.generate()

    def __str__(self) -> str:
        string = ''
        for chromosome in self.chromosomes:
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
            print(farms[i]['avaliable'])
            if not self.isFarmValid(chromosome.shape[i], farms[i]['avaliable']):
                print('is monster')
                return True
        print('is not monster')
        return False

    def isFarmValid(self, culture: list, avaliable: int) -> bool:
        cultivated = (culture[0] * cultivation[0]['cultivated'] +
                      culture[1] * cultivation[1]['cultivated'] +
                      culture[2] * cultivation[2]['cultivated'])
        print(f'cultivated: {cultivated} | avaliable: {avaliable}')
        return (cultivated < avaliable)


p = Population()
print(p)
