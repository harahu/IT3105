#! /usr/bin/python3

import random, sys

"""A collections of functions used in algorithms"""


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

def printSolutions(solutions):
    for solution in solutions:
        print('>>', end=' ')
        for col in solution:
            print(col+1, end=' ')
        print('\n')
    print(str(len(solutions))+" solutions found")

def printBoard(board):
    for col in board:
            print(col+1, end=' ')
        print('\n')


def printRuntime(runTime):
    if runTime < 1:
        runTime = round(runTime, 5)
    elif runTime < 5:
        runTime = round(runTime, 3)
    elif runTime < 10:
        runTime = round(runTime, 2)
    elif runTime < 20:
        runTime = round(runTime, 1)
    else:
        runTime = round(runTime)

    print("Runtime: "+str(runTime)+" seconds")

def repair(board):
    """
    Moves queen that are on the same row
    Input: List
    Output: List
    """
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

def mirrorInvert(board):
    """
    Returns mirrored, inverted and inverted mirrored solutions
    Input: List
    Output: Tuple of List
    """
    inverted = []
    mirrored = []
    inverted_mirrored = []
    for i in range(len(board)):
        inverted.append(len(board)-board[i]-1)
        mirrored.append(board[len(board)-i-1])
        inverted_mirrored.append(len(board)-board[len(board)-i-1]-1)
    
    return (inverted, mirrored, inverted_mirrored)

def expandSolution(board):
    """
    Returns 7 related solutions from one solution
    Input: List
    Output: Tuple of List
    """
    rotatedBoard = board[:]
    for i in range(len(board)):
        rotatedBoard[board[i]] = len(board) - 1 - i
    
    return (rotatedBoard,) + mirrorInvert(rotatedBoard) + mirrorInvert(board)    

def getInput():
    """
    Get input from user or from sys.argv
    Output: List
    """
    if len(sys.argv) == 1:
        int(input("Specify board size: ")) # to meet requirement
        rawBoard = input("Enter board data: ").split(" ")
    else:
        rawBoard = sys.argv[1:]
    board = [int(i)-1 for i in rawBoard]
    return board

def askForStep():
    """
    Ask user if program should be stepped
    Output: Boolean
    """
    answer = input("Run with stepped? (y/N) ")
    if answer == 'y':
        return True
    return False

