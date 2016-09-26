import math, random, time
from tools import *


class BoardState():
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
        """
        Returns a lookup table for number of queens in diagonals and rows
        """
        self.locStates = [[0 for i in range(self.pS.size)], [0 for i in range(2 * self.pS.size - 1)], [0 for i in range(2 * self.pS.size - 1)]]
        for col in range(self.pS.size):
            row = self.board[col]
            self.locStates[0][row] += 1
            #marking NW to SE diagonal as under attack
            self.locStates[1][self.pS.diagCoords[col][row][0]] += 1
            #marking SW to NE diagonal as under attack
            self.locStates[2][self.pS.diagCoords[col][row][1]] += 1

    def energy(self):
        """
        Number of non-attacking queen pairs
        """
        self.energy = self.pS.target
        for locList in self.locStates:
            for line in locList:
                    self.energy -= self.pS.comb[line]

    def neighbour(self):
        """
        Swaps two cols
        """
        cols = random.sample(range(self.pS.size), 2)
        newBoard = self.board[:]
        newBoard[cols[0]] = self.board[cols[1]]
        newBoard[cols[1]] = self.board[cols[0]]
        neighbour = BoardState(self.pS, board=newBoard)
        return neighbour

    def neighbour2(self):
        """
        Moves queen within one col
        """
        col = random.randint(0, self.pS.size-1)
        row = random.randint(0, self.pS.size-1)
        newBoard = self.board[:]
        newBoard[col] = row
        neighbour = BoardState(self.pS, board=newBoard)
        return neighbour

def nQueensSimAnn(pS, bS, itr, initTmp, a):
    """
    Implementation of Simulated Annealing for the n queens domain
    Input: ProblemState, BoardState, int, double/int, double
    Output: Set of tuples
    """
    t = initTmp
    solutions = set([])
    for i in range(itr):
        if bS.energy == pS.target:
            derivates = expandSolution(bS.board)
            for solution in derivates:
                solutions.add(tuple(solution))
        candidate = bS.neighbour()
        dE = bS.energy - candidate.energy
        if (dE < 0) or (math.exp(-(dE/t)) > random.random()):
            bS = candidate
        t *= a
    return solutions
        
def main():
    inBoard = [i for i in range(30)]
    inBoard = repair(inBoard)
    
    pS = ProblemState(len(inBoard))
    bS = BoardState(pS, board=inBoard)
    
    start = time.clock()
    solutions = nQueensSimAnn(pS, bS, 500000, 1000, 0.99)
    end = time.clock()
    printSolutions(solutions)
    printRuntime(end - start)
    
if __name__ == '__main__':
    main()
