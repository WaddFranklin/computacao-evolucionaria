import BTree
import numpy as np

truthTable = [
    {'a': True, 'b': True, 'y': True},
    {'a': True, 'b': False, 'y': False},
    {'a': False, 'b': True, 'y': True},
    {'a': False, 'b': False, 'y': True},
]

dictionary = {
    0: False,
    1: True,
    2: 'OR',
    3: 'AND',
    4: None
}

class Chromosome:

    SIZE = 7
    
    def __init__(self) -> None:
        self.shape = np.random.randint(0, 5, ())