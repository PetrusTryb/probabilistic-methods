from math import inf, sqrt

TASK1_N = 7
TASK2_N = 8
TASK2_K = 4


cities = []
citynames = []

pArray = []
pToAdd = []

cArray = set()
cToAdd = set()


class TreeNode:
    data = -1
    children = []

    def __init__(self, data, children):
        self.data = data
        self.children = children

    def __gt__(self, other):
        return self.data > other.data

    def __lt__(self, other):
        return self.data < other.data
    
class City:
    id = 0
    name = ""
    population = 0
    latitude = 0.0
    longitude = 0.0
    def __init__(self, data):
        self.id = int(data[0])
        self.name = data[1]
        self.population = int(data[2])
        self.latitude = float(data[3])
        self.longitude = float(data[4])
        
    def __str__(self) -> str:
        return self.name
    
    def distance(self, other):
        return sqrt((self.latitude - other.latitude)**2 + (self.longitude - other.longitude)**2)


def read_data(name):
    with open(name, "r") as f:
        f.readline()
        for row in f:
            r = row.split(" ")
            citynames.append(r[1])
            cities.append(City(r))


def permutations(tree_root, my_set, l):
    if (l == 0):
        return
    if len(my_set) == 0:
        return
    for i in my_set:
        newNode = TreeNode(i, [])
        newSet = my_set.copy()
        newSet.remove(i)
        permutations(newNode, newSet, l - 1)
        tree_root.children.append(newNode)
        tree_root.children = sorted(tree_root.children)
        newSet.add(i)


def print_tree(tree_root):
    global pArray, pToAdd
    if (tree_root.data != -1):
        pToAdd.append(tree_root.data)
    if len(tree_root.children) == 0:
        pArray.append(pToAdd.copy())
        pToAdd.clear()
        return
    print_tree(tree_root.children[0])
    if len(tree_root.children):
        if len(tree_root.children[0].children) == 0:
            tree_root.children.remove(tree_root.children[0])
      
def print_tree_combinations(tree_root, l):
    global cArray, cToAdd
    cArray = set()
    cToAdd = set()
    cArray.add(tuple())
    for i in range(0, len(tree_root.children)):
        cToAdd = set()
        cToAdd.add(tree_root.children[i].data)
        cArray.add(tuple(cToAdd))
        for s in cArray.copy():
            s = (*s, tree_root.children[i].data)
            cArray.add(s)
    cArrayCopy = []
    for i in map(set, cArray):
        if len(i)==l:
            cArrayCopy.append(tuple(i))
    cArray = list(frozenset(cArrayCopy))
      
def shortest_cycle():
    global pArray
    minDistance = inf
    minPath = []
    for path in pArray:
        distance = 0
        for i in range(0, len(path)):
            distance += cities[path[i]].distance(cities[path[(i+1)%len(path)]])
        if distance < minDistance:
            minDistance = distance
            minPath = path
    return minPath, minDistance

def partition(tree,target,N):
    bestMatch = inf
    bestSet = []
    bestSetSum = 0
    for length in range(1, N):
        print_tree_combinations(tree,length)
        for subset in cArray:
            subsetPopulation = int(sum(map(lambda x: cities[x].population, subset)))
            if abs(subsetPopulation - target) < bestMatch:
                bestMatch = abs(subsetPopulation - target)
                bestSet = subset
                bestSetSum = subsetPopulation
    return bestSetSum, bestSet

if __name__ == '__main__':
    read_data("france.txt")
    print(list(map(str, cities)))
    tree_root = TreeNode(-1, [])
    permutations(tree_root, set(range(0, TASK1_N)), TASK1_N)
    while len(tree_root.children) > 0:
        print_tree(tree_root)
    pCount = len(pArray)
    print(f"1. Permutations for N={TASK1_N}: ", pCount)
    for i in range(1, pCount+1):
        print(f"{i}. {list(map(lambda x: citynames[x], pArray[i-1]))}")
        
    shortest_cycle_path, shortest_cycle_distance = shortest_cycle()
    print(f"1d. Shortest cycle for N={TASK1_N}: ", shortest_cycle_distance, list(map(lambda x: citynames[x], shortest_cycle_path)))
    
    tree_root = TreeNode(-1, [])
    permutations(tree_root, set(range(0, TASK2_N)), TASK2_N)
    print_tree_combinations(tree_root,TASK2_K)
    cCount = len(cArray)
    print(f"2. Combinations for N={TASK2_N}, K={TASK2_K}: ", cCount)
    cArrayOutput = []
    for i in range(0, cCount):
        cArrayOutput.append(list(map(lambda x: citynames[x], cArray[i])))
    cArrayOutput = sorted(cArrayOutput)
    for i in range(0, cCount):
        print(i+1, cArrayOutput[i])
        
    targetPopulation = sum(map(lambda x: cities[x].population, range(0, TASK2_N)))//2
    bestMatch, bestSet = partition(tree_root,targetPopulation, TASK2_N)
    print(f"2d. Best partition for N={TASK2_N} (target: {targetPopulation}): ", bestMatch, list(map(lambda x: citynames[x], bestSet)))
