with open('wi29.tsp', 'r') as f:
	inp = [line.rstrip('\n') for line in f]
inp = inp[7:len(inp)-1]

for i in range(len(inp)):
	inp[i] = inp[i].split(' ')[1:]

x = []
y = []

for i in inp:
	x.append(float(i[0]))
	y.append(float(i[1]))

x = [float(i)/max(x) for i in x]
y = [float(i)/max(y) for i in y]

print(x)
print(y)