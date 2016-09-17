import time, multiprocessing, copy

class BoardInvalidError(Exception):
    """Exception raised if input board is in a state of attack."""
    pass

class BoardSizeError(Exception):
    """Exception raised if input board size doesn't match with input size"""
    pass

def threadToggle():
    print("N Queens Solver 0.1.1\nbrought to you by Harald Husum")
    threading = input("Multithreading [y/n]: ")
    if threading == "y":
        return True
    else:
        return False

"""Converts board input to format understood by the program."""
def inputBoardProcessing(board):
	board = board.split(' ')
	for i in range(len(board)):
		board[i] = int(board[i])-1
	return board

"""Requests size and board information from user."""
def requestBoardInput():
    size = int(input(">> "))
    board = inputBoardProcessing(input(">> "))
    print("")
    if size != len(board):
        raise BoardSizeError()
    return board

"""Returns the index of the first column that has not been determined by
user. If the board is filled, -1 is returned."""
def startColumn(size, board):
    for col in range(size):
        if board[col] == -1:
            return col
    return -1

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
is initialized with the attack states of the initial board configuration.
Raises BoardInvalidError if the board configuration contains conflicting
queens."""
def locationStates(size, board, diagCoords):
    locStates = [[True for i in range(size)], [True for i in range(2 * size - 1)], [True for i in range(2 * size - 1)]]
    for col in range(size):
        row = board[col]
        if row != -1:
            if locStates[0][row]:
                #marking row as under attack
                locStates[0][row] = False
            else:
                raise BoardInvalidError()
            
            if locStates[1][diagCoords[col][row][0]]:
                #marking NW to SE diagonal as under attack
                locStates[1][diagCoords[col][row][0]] = False
            else:
                raise BoardInvalidError()
            
            if locStates[2][diagCoords[col][row][1]]:
                #marking SW to NE diagonal as under attack
                locStates[2][diagCoords[col][row][1]] = False
            else:
                raise BoardInvalidError()
    return locStates

def nQueensRecBack(size, col, board, diagCoords, locStates, solutions):
    """This is the recursion base case. The board has been filled, and thus we
    have a valid solution to the n queens problem. This is true because our
    procedure invariably allows only non-attacking board entries. The base
    case saves the solution to a list, and returns True to indicate a valid
    solution has been found."""
    if col >= size:
        #collects solution in a list, could alternatively print the solution
        solutions.append(board[:])
        return True
    
    """If the board is not filled, we try out every row position in the
    column, moving deeper in the seach tree if a non-attacking placement is
    found. foundSolution will be set to true if a valid solution is found."""
    foundSolution = False
    for row in range(size): #could i implement row check here?
        #checking availability of row and diagonals
        if (locStates[0][row]
        and locStates[1][diagCoords[col][row][0]]
        and locStates[2][diagCoords[col][row][1]]):
            #placing queen
            board[col]=row
            #marking row as under attack
            locStates[0][row] = False
            #marking NW to SE diagonal as under attack
            locStates[1][diagCoords[col][row][0]] = False
            #marking SW to NE diagonal as under attack
            locStates[2][diagCoords[col][row][1]] = False
            
            #initiate recursion
            if nQueensRecBack(size, col+1, board, diagCoords, locStates, solutions):
                foundSolution = True #a valid solution has been found
            
            board[col]=-1 #removing queen
            locStates[0][row] = True #freeing row
            locStates[1][diagCoords[col][row][0]] = True #freeing nw diagonal
            locStates[2][diagCoords[col][row][1]] = True #freeing sw diagonal
    
    """At this point returnValue is indicative of whether a valid solution has
    been found deeper in the tree. It is passed down the call tree."""
    return foundSolution

def threadedNQueensRecBack(size, col, board, diagCoords, locStates, solutions):
    if col >= size:
        solutions.append(board[:])
        return True
    
    if __name__ == '__main__':
        with multiprocessing.Manager() as manager:
            foundSolutions = []
            processes = []
            for row in range(size):
                if (locStates[0][row]
                and locStates[1][diagCoords[col][row][0]]
                and locStates[2][diagCoords[col][row][1]]):
                    board[col]=row
                    locStates[0][row] = False
                    locStates[1][diagCoords[col][row][0]] = False
                    locStates[2][diagCoords[col][row][1]] = False
            
                    processSolutions = manager.list()
                    foundSolutions.append(processSolutions)
                    processes.append(multiprocessing.Process(target=nQueensRecBack, args=(size, col+1, board[:], copy.deepcopy(diagCoords), copy.deepcopy(locStates[:]), processSolutions)))
            
                    board[col]=-1 #removing queen
                    locStates[0][row] = True #freeing row
                    locStates[1][diagCoords[col][row][0]] = True #freeing nw diagonal
                    locStates[2][diagCoords[col][row][1]] = True #freeing sw diagonal
    
            for process in processes:
                process.start()
            
            for process in processes:
                process.join()
    
            foundSolution = False
            for processSolutions in foundSolutions:
                if processSolutions != []:
                    foundSolution = True
                    for solution in processSolutions:
                        solutions.append(solution)
    
    return foundSolution
    
    
    
    """At this point returnValue is indicative of whether a valid solution has
    been found deeper in the tree. It is passed down the call tree."""
    return foundSolution

"""Helper procedure for solution printing"""
def solutionPrint(solution):
    #change to 1 indexing for readability while also formating for print
    printable = ">> "
    for col in range(len(solution)):
        printable = printable + str(solution[col]+1) + " "
    #print
    print(printable)
    

def main():
    threading = threadToggle()
    try:
        board = requestBoardInput()
    except BoardSizeError:
        print("Error: Board size mismatch")
        return
    size = len(board)
    
    #initiate timing
    start = time.time()
    
    """Fetching the number of the first non-specified column"""
    startCol = startColumn(size, board)
    
    """diagCoords contains precomputed diagonal coordinates for every board
    square. These are looked up by standard coordinates"""
    diagCoords = diagonalCoordinates(size)
    
    """locStates contains the attack status of every row and diagonal on the
    board. Value is set to True if square line is available, False if under
    attack."""
    try:
        locStates = locationStates(size, board, diagCoords)
    except BoardInvalidError:
        print("Error: Board configuration invalid")
        return
    
    """soltions is a holding list for valid board states discovered along the
    way. It is passes as an argument to the recursive backtrack function, to
    be filled out."""
    solutions = []
    
    """Initiate recursive backtrack solver procedure"""
    result = False
    if threading:
        result = threadedNQueensRecBack(size, startCol, board, diagCoords, locStates, solutions)
    else:
        result = nQueensRecBack(size, startCol, board, diagCoords, locStates, solutions)
    if result:
        #terminate timing
        end = time.time()
        # print solutions
        for solution in solutions:
            solutionPrint(solution)
        # print number of solutions
        print("\nSolutions found: "+str(len(solutions)))
        #print timing
        print("Runtime: "+str(end - start)+" seconds\n")
    else:
        print("Error: No valid solution exists")

main()