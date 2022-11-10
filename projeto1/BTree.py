'''
    operations:
        AND = 3
        OR = 2
    Leaves:
        True
        False
'''
convert = {
    0: 'False',
    1: 'True',
    2: 'OR',
    3: 'AND',
}

class BTree:
    
    def __init__(self, value=False, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        

def buildBTree(input: list) -> BTree:
    
    if len(input) > 0:
        item = input.pop(0)
        
        if item == None:
            return None
        elif item == 1 or item == 0:
            return BTree(item)
        else:
            bt = BTree(item)
            bt.left = buildBTree(input)
            bt.right = buildBTree(input)
            
        return bt
    
def toString(value: int) -> str:
    return convert[value] if (value == 0 or value == 1) else (' ' + convert[value] + ' ')

def isEmpty(bt: BTree):
    return bt == None

def isLeaf(bt: BTree):
    return bt.left == None and bt.right == None

def printBTree(bt: BTree):
    if not isEmpty(bt):
        if not isLeaf(bt) and (isLeaf(bt.left) and isLeaf(bt.right)):
            print('(', end='')
            printBTree(bt.left)
            print(toString(bt.value), end='')
            printBTree(bt.right)
            print(')', end='')
        else:
            printBTree(bt.left)
            print(toString(bt.value), end='')
            printBTree(bt.right)
            
def evaluate(bt: BTree):
    if isLeaf(bt):
        return bool(bt.value)
    
    if bt.value == 2:
        return evaluate(bt.left) or evaluate(bt.right)
    else:
        return evaluate(bt.left) and evaluate(bt.right)
        

input = [2, 3, 1, 1, 2, 0, 0]
bt = buildBTree(input)
printBTree(bt)
print(f' = {str(evaluate(bt))}')