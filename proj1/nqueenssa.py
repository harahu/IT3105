import math, random, time
        
"""Returns a lookup table of diagonal coordinates for each board square. In
this context a diagonal coordinate is the diagonal number for the sqare, both
from NW to SE and SW to NE, ordered from west to east. Coordinate location in
the table is given by standard column and rom number."""
def diagonalCoordinates(size):
    diagCoords = [[[0 for i in range(2)] for j in range(size)] for k in range(size)]
    for col in range(size):
        for row in range(size):
            #NW to SE diagonal
            diagCoords[col][row][0] = col - row + size - 1
            #SW to NE diagonal
            diagCoords[col][row][1] = col + row
    return diagCoords

"""Returns a lookup table for attack states of rows and diagonals. The table
is initialized with the attack states of the initial board configuration."""
def locationStates(size, board, diagCoords):
    locStates = [[True for i in range(2 * size - 1)], [True for i in range(2 * size - 1)]]
    for col in range(size):
        row = board[col]
        #marking NW to SE diagonal as under attack
        locStates[0][diagCoords[col][row][0]] = False
        #marking SW to NE diagonal as under attack
        locStates[1][diagCoords[col][row][1]] = False
    return locStates

def nrgFunc(locStates):
    energy = 0
    for diagList in locStates:
        for diagonal in diagList:
            if not diagonal:
                energy += 1
    return energy

def neighbour(board, diagCoords, locStates):
    newBoard = board
    switch = random.sample(range(len(board)), 2)
    hold = newBoard[switch[0]]
    newBoard[switch[0]] = newBoard[switch[1]]
    newBoard[switch[1]] = hold
    newLocStates = locationStates(len(newBoard), newBoard, diagCoords)
    return [newBoard, newLocStates]

def neighbourStrict(board, diagCoords, locStates):
    newBoard = board
    switch = random.randint(0, len(board)-1)
    hold = newBoard[switch]
    if switch < len(board)-1:
        newBoard[switch] = newBoard[switch+1]
        newBoard[switch+1] = hold
    else:
        newBoard[switch] = newBoard[0]
        newBoard[0] = hold
    newLocStates = locationStates(len(newBoard), newBoard, diagCoords)
    return [newBoard, newLocStates]

def neighbourStrict2(board, diagCoords, locStates):
    newBoard = board
    switch = random.randint(0, len(board)-2)
    hold = newBoard[switch]
    newBoard[switch] = newBoard[switch+1]
    newBoard[switch+1] = hold
    newLocStates = locationStates(len(newBoard), newBoard, diagCoords)
    return [newBoard, newLocStates]

def nQueensSimAnn(board, diagCoords, locStates, iterations):
    t = 30
    for i in range(iterations):
        energy = nrgFunc(locStates)
        if energy == len(board)*2:
            return board
        t *= 0.995
        accept = False
        j = 0
        while not accept:
            j += 1
            candidate = neighbourStrict2(board, diagCoords, locStates)
            dE = nrgFunc(locStates) - nrgFunc(candidate[1])
            if dE <= 0:
                board = candidate[0]
                locStates = candidate[1]
                accept = True
            else:
                if math.exp(-(dE/t)) > random.random():
                    board = candidate[0]
                    locStates = candidate[1]
                    accept = True
        #print(j)
    return board
        
def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    """diagCoords contains precomputed diagonal coordinates for every board
    square. These are looked up by standard coordinates"""
    diagCoords = diagonalCoordinates(len(board))
    
    """locStates contains the attack status of every diagonal on the
    board. Value is set to True if square line is available, False if under
    attack."""
    locStates = locationStates(len(board), board, diagCoords)
    start = time.clock()
    for i in range(100):
        solution = nQueensSimAnn(board, diagCoords, locStates, 100000)
    end = time.clock()
    print("Runtime: "+str(end - start)+" seconds\n")
    for i in range(len(solution)):
        solution[i] += 1
    print(solution)
    

main()