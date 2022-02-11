from FPTree import *
import sys

def read_labels(filename):
    with open(filename, 'r') as fd:
        lines = [line.split() for line in fd if (len(line) > 0)]
        return dict((int(line[0]), "".join(line[1:])) for line in lines)

# Reads a file into a 2d list
def load_data(filename):
    with open(filename, 'r') as fd:
        dataset = [list(map(int, line.strip().split())) for line in fd if len(line) != 0]
        
    return dataset

# Main fpgrowth calculation algorithm
# It constructs and mines tree and returns a dictionary with frequent item list and counts
def fpgrowth(dataset, support):
    #sup = len(dataset) * support
    sup = support
    
    fptree = FPTree()
    tree, headerTable = fptree.ConstructTree(dataset, sup)

    if (tree == None):
        print("No frequent sets")
        return

    freqIt = fptree.MineTree(headerTable, sup)
    freqIt = dict((key, value) for key, value in freqIt.items() if len(key) > 1)
    return freqIt
    
    
