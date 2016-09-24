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

    """
    def neighbour(self):
        if self.req == 0:
            self.neighbourOrder = []
            for i in range(self.pS.size):
                for j in range(self.pS.size):
                    if j<=i:
                        pass
                    self.neighbourOrder.append([i, j])
            random.shuffle(self.neighbourOrder)
        if self.req >= len(self.neighbourOrder):
            self.req = 0
        newBoard = self.board[:]
        switch = self.neighbourOrder[self.req]
        hold = newBoard[switch[0]]
        newBoard[switch[0]] = newBoard[switch[1]]
        newBoard[switch[1]] = hold
        neighbour = boardState(self.pS, board=newBoard)
        self.req += 1
        return neighbour

    def neighbour(self):
        newBoard = self.board[:]
        switch = random.randint(0, self.pS.size-2)
        hold = newBoard[switch]
        newBoard[switch] = newBoard[switch+1]
        newBoard[switch+1] = hold
        neighbour = boardState(self.pS, board=newBoard)
        return neighbour

    def neighbour(self):
        cut = random.randint(1, self.pS.size-1)
        newBoard = self.board[cut:]+self.board[:cut]
        neighbour = boardState(self.pS, board=newBoard)
        return neighbour
    """

def nQueensSimAnn(pS, bS, iterations):
    t0 = 30
    t = 0
    for i in range(1, iterations):
        t = t0/(i/3)
        if bS.energy == pS.target:
            print("success")
            print(i)
            return bS
        candidate = bS.neighbour()
        dE = bS.energy - candidate.energy
        if (dE <= 0) or (math.exp(-(dE/t)) > random.random()):
            bS = candidate
    print("failed")
    print(t)
    return bS
        
def main():
    inBoard = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    
    pS = problemState(len(inBoard))

    bS = boardState(pS, board=inBoard)
    
    start = time.clock()
    for i in range(1):
        solution = nQueensSimAnn(pS, bS, 10000000)
    end = time.clock()
    print("Runtime: "+str(end - start)+" seconds\n")
    print(solution.locStates)
    solution = solution.board
    for i in range(len(solution)):
        solution[i] += 1
    print(solution)
    
if __name__ == '__main__':
    main()
