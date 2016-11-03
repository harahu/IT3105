import math, random

def get_problem_set(filename):
    """Returns a list of max-normalized city coordinates"""
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

def euclidian_distance(a, b):
    return math.sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))

def get_best_match_index(city, neuron_list):
    best = 0
    best_dist = 0

    for i in range(len(neuron_list)):
        distance = euclidian_distance(city, neuron_list[i])
        if distance > best_dist:
            best = i
            best_dist = distance

    return best

def train(weight, city, alpha, discount):
    weight[0] += alpha*discount*(city[0]-weight[0])
    weight[1] += alpha*discount*(city[1]-weight[1])

def main():
    #initialization
    cities = get_problem_set('uy734.tsp')
    som_ring = [[random.random() for i in range(2)] for i in range(len(cities))]
    eta = 0.8
    delta = 6.2 + 0.037*len(cities)
    n_iterations = 50*len(cities)

    for i in range(n_iterations):
        city = random.choice(cities)
        match = get_best_match_index(city, som_ring)

        #train
        train(som_ring[match], city, eta, 1)
        for distance in range(1, math.ceil(delta)):
            discount = (1-distance/delta)
            train(som_ring[(match+distance) % len(som_ring)], city, eta, discount)
            train(som_ring[(match-distance) % len(som_ring)], city, eta, discount)

        #update parameters
        eta -= (0.8/n_iterations)
        if delta > 1:
            delta -= (6.2 + 0.037*len(cities))/(n_iterations*0.65)
        else:
            delta = 1
    print("TADA!")

if __name__ == '__main__':
    main()
