import random

def get_problem_set(filename):    
    with open(filename, 'r') as f:
        inp = [line.rstrip('\n') for line in f]
    inp = inp[7:len(inp)-1]

    for i in range(len(inp)):
        inp[i] = inp[i].split(' ')[1:]
        inp[i] = [float(j) for j in inp[i]]

    max_x = max(city[0] for city in inp)
    max_y = max(city[1] for city in inp)

    inp = [[city[0]/max_x, city[1]/max_y] for city in inp]

    return inp

def get_best_match_index(city, neuron_list):
    best = 0
    best_val = 0

def main():
    #initialization
    cities = get_problem_set('wi29.tsp')
    som_ring = [[random.random() for i in range(2)] for i in range(len(cities))]
    city = random.randrange(0, len(cities))

    match = get_best_match_index(city, som_ring) #index?
    #train m and neighbours
    #update parame


if __name__ == '__main__':
    main()
