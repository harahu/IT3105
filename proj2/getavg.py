import sys

f = open(sys.argv[1], 'r').readlines()

a = []
for i in f:
    a.append(int(i))

print(sum(a)/len(a))
