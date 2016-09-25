#! /usr/bin/python3

import random

"""A collections of functions used in algorithms"""

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
    board = [int(i) for i in rawBoard]
    return board

