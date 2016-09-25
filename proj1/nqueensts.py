import math, random, time

class ProblemState():
    """Contains information dependent on problem size to be looked up.
    Should not be changed after initialization."""
    def __init__(self, size):
        self.size = size
        self.comb = ProblemState.nC2List(size + 1)
        self.target = self.comb[size]
        self.diagCoords = ProblemState.diagonalCoordinates(size)

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

class BoardState():
    def __init__(self, pS, **kwargs):
        self.pS = pS
        self.board = kwargs.get('board')
        if self.board is not None:
            self.locationStates()
            self.energy()
            self.req = 0

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

    def neighbours(self):
        """Returns a list of moves to get to neighbours"""
        temp = []
        # get neighbours by swapping columns
        for col0 in range(self.pS.size-1):
            for col1 in range(col0+1, self.pS.size):
                temp.append((col0, col1))
        
        return temp
    
    def doMove(self, move):
        """Executes a move on a copy of board, and returns it"""
        tempBoard = self.board[:]
        tempBoard[move[0]] = self.board[move[1]]
        tempBoard[move[1]] = self.board[move[0]]
        
        return BoardState(self.pS, board=tempBoard)
        
class TabuState():
    """Contains functions and memory for tabu search"""
    def __init__(self, pS, maxTabu):
        self.tabuList = [None] * maxTabu
        self.index = 0
        self.maxTabu = maxTabu
        self.moveCount = {}
    
    def insertTabu(self, item):
        print("index: " + str(self.index) + " max: " + str(self.maxTabu))
        self.tabuList[self.index % self.maxTabu] = item
        self.index += 1
        try:
            self.moveCount[item] += 1
        except KeyError:
            self.moveCount[item] = 1
        
    
    

def nQueensTabuSearch(pS, bS, tS, iterations):
    currentBoard = bS
    bestBoard = bS
    
    for i in range(iterations):
        print("iteration: "+str(i))
        neighbours = currentBoard.neighbours()
        
        # Find best neighbour not in tabu list
        curBest = -10000
        bestNeighbour = None
        bestMove = None
        for nMove in neighbours:
            neighbour = currentBoard.doMove(nMove)
            if nMove in tS.tabuList and neighbour.energy < currentBoard.energy: # Aspiration criterion
                continue
            
            try:
                nValue = neighbour.energy - tS.moveCount[nMove]
            except KeyError:
                nValue = neighbour.energy
            
            if nValue > curBest:
                curBest = nValue
                bestNeighbour = neighbour
                bestMove = nMove
        
        if bestNeighbour == None:
            print("Could not find a new neighbours")
            return bestBoard
        
        if bestNeighbour.energy > currentBoard.energy:
            currentBoard = bestNeighbour
        
        if bestNeighbour.energy > bestBoard.energy:
            bestBoard = bestNeighbour
        
        tS.insertTabu(bestMove)
    
    return bestBoard

def main():
    startBoard = [i for i in range(6)]
    
    pS = ProblemState(len(startBoard))
    bS = BoardState(pS, board=startBoard)
    tS = TabuState(pS, 4)
    
    startTime = time.clock()
    solution = nQueensTabuSearch(pS, bS, tS, 1000)
    endTime = time.clock()
    
    print(solution.locStates)
    print(solution.energy)
    print(pS.target)
    
    print("Runtime: "+str(endTime - startTime)+" seconds\n")
    print(solution.board)
    


if __name__ == '__main__':
    main()
