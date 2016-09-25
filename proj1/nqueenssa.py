import math, random, time

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
            self.locationStates()
            self.energy()
            self.req = 0
        else:
            self.parent = kwargs.get('parent')
            self.change = kwargs.get('change')

    def locationStates(self):
        """Returns a lookup table for number of queens in diagonals and horizontals"""
        self.locStates = [[0 for i in range(self.pS.size)], [0 for i in range(2 * self.pS.size - 1)], [0 for i in range(2 * self.pS.size - 1)]]
        for col in range(self.pS.size):
            row = self.board[col]
            self.locStates[0][row] += 1
            #marking NW to SE diagonal as under attack
            self.locStates[1][self.pS.diagCoords[col][row][0]] += 1
            #marking SW to NE diagonal as under attack
            self.locStates[2][self.pS.diagCoords[col][row][1]] += 1

    def energy(self):
        self.energy = self.pS.target
        for locList in self.locStates:
            for line in locList:
                    self.energy -= self.pS.comb[line]

    def neighbour(self):
        col = random.randint(0, self.pS.size-1)
        row = random.randint(0, self.pS.size-1)
        newBoard = self.board[:]
        newBoard[col] = row
        neighbour = boardState(self.pS, board=newBoard)
        return neighbour

    def neighbour2(self):
        cols = random.sample(range(self.pS.size), 2)
        newBoard = self.board[:]
        newBoard[cols[0]] = self.board[cols[1]]
        newBoard[cols[1]] = self.board[cols[0]]
        neighbour = boardState(self.pS, board=newBoard)
        return neighbour

def nQueensSimAnn(pS, bS, iterations):
    t = 1000
    a = 0.99
    solutions = set([])
    for i in range(1, iterations):
        if bS.energy == pS.target:
            solutions.add(tuple(bS.board))
        candidate = bS.neighbour2()
        dE = bS.energy - candidate.energy
        if (dE < 0) or (math.exp(-(dE/t)) > random.random()):
            bS = candidate
        t *= 0.99
    return solutions
        
def main():
    inBoard = [i for i in range(30)]
    
    pS = problemState(len(inBoard))

    bS = boardState(pS, board=inBoard)
    
    start = time.clock()
    solutions = nQueensSimAnn(pS, bS, 500000)
    print(len(solutions))
    end = time.clock()
    print("Runtime: "+str(end - start)+" seconds\n")
    
if __name__ == '__main__':
    main()
