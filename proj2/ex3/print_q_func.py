import os, sys
import json

# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

qfuncjson = open(sys.argv[1], 'r').read()
qtable = json.loads(qfuncjson)

table = [['S','F','F','F'],
         ['F','H','F','H'],
         ['F','F','F','H'],
         ['H','F','F','G']]

table[0][0] = bcolors.OKGREEN + 'S' + bcolors.ENDC
table[3][3] = bcolors.HEADER + 'G' + bcolors.ENDC

for row in range(4):
    for col in range(4):
        if table[row][col] == 'F':
            table[row][col] = bcolors.OKBLUE + 'F' + bcolors.ENDC
        if table[row][col] == 'H':
            table[row][col] = bcolors.FAIL + 'H' + bcolors.ENDC

for row in range(4):
    # print 1. line
    print("\n +", end='')
    for col in range(4):
        print("------------+", end='')
    
    # print 2. line
    print("\n |", end='')
    for col in range(4):
        print("    %.2f    |"%(qtable[4*row+col][3]), end='')
    
    # print 3. line
    print("\n |", end='')
    for col in range(4):
        print("            |", end='')
    
    # print 4. line
    print("\n |", end='')
    for col in range(4):
        print("%.2f %s %.2f|"%(qtable[4*row+col][0], table[row][col]*2, qtable[4*row+col][2]), end='')
    
    # print 5. line
    print("\n |", end='')
    for col in range(4):
        print("            |", end='')
    
    # print 6. line
    print("\n |", end='')
    for col in range(4):
        print("    %.2f    |"%(qtable[4*row+col][1]), end='')
    
    # print 7. line
    print("\n +", end='')
    for col in range(4):
        print("------------+", end='')

print()
