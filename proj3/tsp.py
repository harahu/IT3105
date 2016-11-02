import random

def get_problem_set(filename):    
    with open(filename, 'r') as f:
        inp = [line.rstrip('\n') for line in f]
    inp = inp[7:len(inp)-1]

    for i in range(len(inp)):
        inp[i] = inp[i].split(' ')[1:]

    x, y = [], []

    for i in inp:
        x.append(float(i[0]))
        y.append(float(i[1]))

    x = [float(i)/max(x) for i in x]
    y = [float(i)/max(y) for i in y]

    return x, y

def get_best_match(city, neuron_list):



def main():
    x, y = get_problem_set('wi29.tsp')
    som_ring = [[random.random() for i in range(2)] for i in range(len(x))]
    city = random.randrange(0, len(x))
    match = get_best_match(city, som_ring) #index?
    #train m and neighbours
    #update parameters


if __name__ == '__main__':
    main()
