import os, sys
import json


qfuncjson = open(sys.argv[1], 'r').read()
qtable = json.loads(qfuncjson)

table = ["SFFF",
         "FHFH",
         "FFFH",
         "HFFG"]

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
