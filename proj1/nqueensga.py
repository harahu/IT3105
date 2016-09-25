import random

class problemState():
    """Contains information dependent on problem size to be looked up.
    Should not be changed after initialization."""
    def __init__(self, size):
        self.size = size
        self.comb = problemState.nC2List(size + 1)
        self.target = self.comb[size]
        self.diagCoords = problemState.diagonalCoordinates(size)

    def nC2List(n):
        """List of n choose 2 from 0 to n"""
        l = []
        for i in range(n):
            l.append(int(i*(i-1)/2))
        return(l)

    def diagonalCoordinates(size):
        """Returns a lookup table of diagonal coordinates for each board square. In
        this context a diagonal coordinate is the diagonal number for the sqare, both
        from NW to SE and SW to NE, ordered from west to east. Coordinate location in
        the table is given by standard column and rom number."""
        diagCoords = [[[0 for i in range(2)] for j in range(size)] for k in range(size)]
        for col in range(size):
            for row in range(size):
                #NW to SE diagonal
                diagCoords[col][row][0] = col - row + size - 1
                #SW to NE diagonal
                diagCoords[col][row][1] = col + row
        return diagCoords

class boardState():
    def __init__(self, pS, **kwargs):
        self.pS = pS
        self.board = kwargs.get('board')
        if self.board is not None:
            self.locationStates();
            self.energy()
            self.req = 0

    def locationStates(self):
        """Returns a lookup table for number of queens in a given diagonal"""
        self.locStates = [[0 for i in range(2 * self.pS.size - 1)], [0 for i in range(2 * self.pS.size - 1)]]
        for col in range(self.pS.size):
            row = self.board[col]
            #marking NW to SE diagonal as under attack
            self.locStates[0][self.pS.diagCoords[col][row][0]] += 1
            #marking SW to NE diagonal as under attack
            self.locStates[1][self.pS.diagCoords[col][row][1]] += 1

    def energy(self):
        self.energy = self.pS.target
        for locList in self.locStates:
            for line in locList:
                    self.energy -= self.pS.comb[line]

    def mutate(self):
        col1 = random.randint(0, self.pS.size-1)
        col2 = random.randint(0, self.pS.size-1)
        newBoard = self.board[:]
        newBoard[col1] = self.board[col2]
        newBoard[col2] = self.board[col1]
        neighbour = boardState(self.pS, board=newBoard)
        return neighbour

def repair(board):
    rows = [0 for i in range(len(board))]
    fix = [False for i in range(len(board))]
    repaired = [-1 for i in range(len(board))]
    for i in range(len(board)):
        if rows[board[i]] == 0:
            repaired[i] = board[i]
        else:
            fix[i] = True
        rows[board[i]] += 1
    unused = []
    for i in range(len(rows)):
        if rows[i] == 0:
            unused.append(i)
    random.shuffle(unused)
    j = 0
    for i in range(len(fix)):
        if fix[i]:
            repaired[i] = unused[j]
            j += 1
    return repaired



def initializePopulation(bS, pS, popSize):
    population = []
    repaired = repair(bS.board)
    bS = boardState(pS, board=repaired)
    population.append(bS)
    for i in range(popSize-1):
        derivative = bS.mutate().mutate().mutate()
        population.append(derivative)
    return population

def rouletteWheelSelection(population, pointers):
    keep = []
    for p in pointers:
        i = 0
        fSum = population[0].energy
        while fSum < p:
            i += 1
            fSum+=population[i].energy
        keep.append(population[i])
    return keep


def stocasticUniversalSampling(population, n):
    f = 0
    for individual in population:
        f += individual.energy
    pD = f//n
    sP = random.randint(0, pD)
    pointers = [(sP + i*pD) for i in range(n-1)]
    return rouletteWheelSelection(population, pointers)

def crossover(p1, p2, pS):
    cb = [i for i in range(pS.size)]
    random.shuffle(cb)
    for i in range(pS.size):
        if p1.board[i] == p2.board[i]:
            for j in range(pS.size):
                if cb[j] == p1.board[i]:
                    cb[j] = cb[i]
                    cb[i] = p1.board[i]
    child = boardState(pS, board=cb)
    return child

def reproduce(parents, n, crossRate, mutationRate, pS):
    children = []
    for i in range(n):
        parent = parents[(i % len(parents))]
        if random.random() <= crossRate:
            randParent = parents[random.randint(0, len(parents)-1)]
            child = crossover(parent, randParent, pS)
        else:
            child = parent
        if random.random() < mutationRate:
            child = child.mutate()
        children.append(child)
    return children

def tourney(pop):
    best = None
    maxEng = 0
    for bS in pop:
        if bS.energy > maxEng:
            best = bS
            maxEng = bS.energy
    return best


def nQueensGenAlg(initPop, pS, itr):
    population = initPop
    solutions = set([])
    for i in range(itr):
        for bS in population:
            if bS.energy == pS.target:
                solutions.add(tuple(bS.board))
                #print(tuple(bS.board))
        children = []
        for i in range(len(initPop)):
            tourn1 = stocasticUniversalSampling(population, 3)
            p1 = tourney(tourn1)
            tourn2 = stocasticUniversalSampling(population, 3)
            p2 = tourney(tourn2)
            child = crossover(p1, p2, pS)
            if random.random() < 0.02:
                child = child.mutate()
            children.append(child)
        population = children

        #population = reproduce(parents, 20, 0.80, 0.01, pS)
    for board in population:
        print(pS.target - board.energy)
    return solutions

def main():
    inBoard = [i for i in range(30)]
    pS = problemState(len(inBoard))
    bS = boardState(pS, board=inBoard)
    initPop = initializePopulation(bS, pS, 100)
    solutions = nQueensGenAlg(initPop, pS, 1000)
    print(solutions)

if __name__ == '__main__':
    main()
