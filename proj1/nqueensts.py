import math, random, time, sys
from tools import *


class BoardState():
    """Contains board data plus functions to calculate neighbours copy board"""
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
        """Calculate energy (fitness) for board"""
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
        #print("index: " + str(self.index) + " max: " + str(self.maxTabu))
        self.tabuList[self.index % self.maxTabu] = item
        self.index += 1
        try:
            self.moveCount[item] += 1
        except KeyError:
            self.moveCount[item] = 1
        

def nQueensTabuSearch(pS, bS, tS, iterations, ltmWeight=0.1, steps=False):
    """Runs tabu search on boardState, bS"""
    currentBoard = bS
    bestBoard = bS
    solutions = set()
    
    print("Starting board: ", end='') if steps else 0
    printBoard(bS.board) if steps else 0
    
    for i in range(iterations):
        print("iteration: "+str(i), end='') if steps else 0
        input() if steps else 0
        neighbours = currentBoard.neighbours()
        
        # Find best neighbour not in tabu list
        curBest = -10000
        bestNeighbour = None
        bestMove = None
        for nMove in neighbours:
            neighbour = currentBoard.doMove(nMove)
            print(str(nMove), end='') if steps else 0
            if nMove in tS.tabuList and neighbour.energy <= currentBoard.energy: # Aspiration criterion
                print(" in tabulist, skipping") if steps else 0
                continue
            elif nMove in tS.tabuList and neighbour.energy > currentBoard.energy:
                print(" in tabulist, but", end='') if steps else 0
            print(" is being considered") if steps else 0
            try:
                nValue = neighbour.energy - ltmWeight * tS.moveCount[nMove]
            except KeyError: # KeyError occures when current move is not in tabu list
                nValue = neighbour.energy
            
            if nValue > curBest:
                curBest = nValue
                bestNeighbour = neighbour
                bestMove = nMove
        print("Best move " + str(bestMove)) if steps else 0
        if bestNeighbour == None:
            print("Could not find a new neighbours")
            return solutions
        
        if bestNeighbour.energy >= currentBoard.energy:
            currentBoard = bestNeighbour
        
        if bestNeighbour.energy > bestBoard.energy:
            bestBoard = bestNeighbour
        
        if bestNeighbour.energy == pS.target:
            solutions.add(tuple(bestNeighbour.board))
            for s in expandSolution(bestNeighbour.board):
                solutions.add(tuple(s))
            print(len(solutions), end='\r')
        
        tS.insertTabu(bestMove)
    
    return solutions


def main():
    steps = askForStep()
    startBoard = getInput()
    #startBoard = [i for i in range(30)]
    startBoard = repair(startBoard)
    
    pS = ProblemState(len(startBoard))
    bS = BoardState(pS, board=startBoard)
    tS = TabuState(pS, 3)
    
    startTime = time.clock()
    solutions = nQueensTabuSearch(pS, bS, tS, 1000, ltmWeight=0.1, steps=steps)
    endTime = time.clock()

    printRuntime(endTime-startTime)
    print("Found " + str(len(solutions)) + " solutions")
    
    

if __name__ == '__main__':
    main()
