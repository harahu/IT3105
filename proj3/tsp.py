import math, random
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sys


# for animation
fig = plt.figure(1)
ax = plt.axes(xlim=(-0.2,1.2), ylim=(-0.2,1.2))
cities_plt, = ax.plot([], [], 'ro', zorder=2, alpha=0.4)
neurons_plt, = ax.plot([], [], 'yo-', zorder=1)
distance_text = ax.text(-0.1, -0.1, "", transform=ax.transAxes)

def get_problem_set(filename):
    """Returns a list of city coordinates together with the 0,1-normalized version"""
    with open(filename, 'r') as f:
        inp = [line.rstrip('\n') for line in f]
    start = inp.index("NODE_COORD_SECTION") + 1
    end = inp.index("EOF")
    inp = inp[start:end]

    for i in range(len(inp)):
        inp[i] = inp[i].split(' ')[1:]
        inp[i] = [float(j) for j in inp[i]]

    max_x = max(city[0] for city in inp)
    min_x = min(city[0] for city in inp)
    max_y = max(city[1] for city in inp)
    min_y = min(city[1] for city in inp)

    inp_norm = [[(city[0]-min_x)/(max_x-min_x), (city[1]-min_y)/(max_y-min_y)] for city in inp]

    return inp, inp_norm

def plot_som_tsp(cities, raw_cities, neurons, fname):
    plt.figure(2)
    plt.clf()
    x0 = [city[0] for city in cities]
    y0 = [city[1] for city in cities]
    x1 = [neuron[0] for neuron in neurons]
    y1 = [neuron[1] for neuron in neurons]
    x1.append(x1[0])
    y1.append(y1[0])
    d = calculate_total_distance(neurons, cities, raw_cities)
    ax2 = plt.axes(xlim=(-0.2,1.2), ylim=(-0.2,1.2))
    cities_plt2, = ax2.plot(x0, y0, 'ro', zorder=2, alpha=0.4)
    neurons_plt2, = ax2.plot(x1, y1, 'yo-', zorder=1)
    distance_text2 = ax2.text(-0.1, -0.1, "Distance: %0.4f" %d, transform=ax2.transAxes)
    plt.savefig("./plots/%s" %fname)
    plt.figure(1)

def init_anim(cities):
    cities_plt.set_data([], [])
    
    x = [city[0] for city in cities]
    y = [city[1] for city in cities]
    cities_plt.set_data(x, y)

def animate(i, neurons, distances):
    neurons_plt.set_data([], [])
    
    x = neurons[i][0]
    y = neurons[i][1]
    
    neurons_plt.set_data(x, y)
    distance_text.set_text("Distance: %0.4f" %(distances[i]))
    return cities_plt, neurons_plt, distance_text

def add_anim(neurons_data, distance_data, neurons, cities, raw_cities):
    x = [neuron[0] for neuron in neurons]
    y = [neuron[1] for neuron in neurons]
    
    x.append(neurons[0][0])
    y.append(neurons[0][1])
    
    neurons_data.append((x,y))
    distance_data.append(calculate_total_distance(neurons, cities, raw_cities))

def print_diagnostics(i, n_iterations, eta, delta):
    print("Progress: %i%%" %(round(100*i/n_iterations)))
    print("Eta: %f" %(eta))
    print("Delta: %f" %(delta), end='\033[F\033[F')
    if i == n_iterations-1:
        print('\n\n\n----------')

def euclidian_distance(a, b):
    return math.sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))

def euclidian_potential(a, b):
    return ((a[0]-b[0])**2)+((a[1]-b[1])**2)

def get_best_match_index(city, neurons, disregard):
    best = 0
    best_pot = euclidian_potential(city, neurons[0])

    for i in range(1, len(neurons)):
        if i in disregard:
            continue
        potential = euclidian_potential(city, neurons[i])
        if potential < best_pot:
            best = i
            best_pot = potential
            
    return best

# Returns list of the closest cities per neuron
def get_closest_city_list(som_ring, cities):
    closest_list = [None] * len(som_ring)
    
    # Add closest neuron for each city
    for city_index in range(len(cities)):
        closest_neuron = get_best_match_index(cities[city_index], som_ring, [])
        closest_list[closest_neuron] = city_index
    
    return closest_list

def calculate_total_distance(som_ring, cities, raw_cities):
    total_distance = 0
    closest_list = get_closest_city_list(som_ring, cities)
    closest_list = [cty for cty in closest_list if cty != None] # filter None neurons
    
    last_city = closest_list[0]
    for city in closest_list:
        total_distance += euclidian_distance(raw_cities[city], raw_cities[last_city])
        last_city = city
    
    total_distance += euclidian_distance(raw_cities[closest_list[0]], raw_cities[last_city])
    
    return total_distance
    
def train(weight, city, alpha, discount):
    weight[0] += alpha*discount*(city[0]-weight[0])
    weight[1] += alpha*discount*(city[1]-weight[1])

def linear_decay(last, initial, n_iterations, end_factor):
    """Returns the next step in a lineary decaying function.
    end_factor indicates at what fraction of the training process
    the function should reach 0"""
    return last - initial/(n_iterations*end_factor)

def exponential_decay(initial, itr, factor):
    """Returns the next step in a exponential decay function."""
    return initial*math.exp(-(itr/factor))

def main():
    #initialization
    files = ("sets/wi29.tsp", "sets/dj38.tsp", "sets/qa194.tsp", "sets/uy734.tsp")
    tspfile = files[2]
    if len(sys.argv) == 2:
        tspfile = sys.argv[1]
    raw_cities, cities = get_problem_set(tspfile)
    #som_ring = [[random.random() for i in range(2)] for i in range(len(cities))]
    som_ring = []
    pick_list = cities[:]
    inhibit = []
    n_neurons = len(cities)*2
    for i in range(n_neurons):
        tetha = i / n_neurons * 2 * math.pi
        som_ring.append([math.cos(tetha)/2 + 0.5, math.sin(tetha)/2 + 0.5])
    init_eta = 0.8 #learning rate
    eta = init_eta
    init_delta = 6.2*2 + 0.037*2*len(cities) #neighbourhood radius
    delta = init_delta
    n_iterations = 100*len(cities)
    decay_type = 1
    frame_step = len(cities)
    
    # for animation plot
    neurons_data = []
    distance_data = []
    add_anim(neurons_data, distance_data, som_ring, cities, raw_cities)
    #plot_som_tsp(cities, raw_cities, som_ring, "start.png")
    
    for i in range(n_iterations):
        if i % len(cities) == 0:
            random.shuffle(pick_list)
            inhibit = []
        city = pick_list[i%len(cities)]
        match = get_best_match_index(city, som_ring, inhibit)
        inhibit.append(match)
        #train
        train(som_ring[match], city, eta, 1)
        for distance in range(1, math.ceil(delta)):
            discount = (1-distance/delta)
            train(som_ring[(match+distance) % len(som_ring)], city, eta, discount)
            train(som_ring[(match-distance) % len(som_ring)], city, eta, discount)

        #update parameters
        if decay_type == 0:
            #static
            pass
        elif decay_type == 1:
            #linear
            eta = linear_decay(eta, init_eta, n_iterations, 1)
            #should reach 1 by 65% competion
            delta = linear_decay(delta, init_delta-1, n_iterations, 0.65)
            if delta < 1:
                delta = 1
        elif decay_type == 2:
            #exponential
            eta = exponential_decay(init_eta, i, len(cities)*15)
            delta = exponential_decay(init_delta, i, len(cities)*15)
            if delta < 1:
                delta = 1
        else:
            print('What are you even trying to do? -_-')

        if (i+1) % frame_step == 0:
            print_diagnostics(i, n_iterations, eta, delta)
            add_anim(neurons_data, distance_data, som_ring, cities, raw_cities)

    #plot_som_tsp(cities, raw_cities, som_ring, "end.png")
    init_anim(cities)
    ani = anim.FuncAnimation(fig, animate, frames=len(neurons_data), fargs=(neurons_data,distance_data,))
    
    plt.show()
    try:
        print("Saving video...")
        ani.save("./animations/%s.mp4" %(tspfile[5:-4]), fps=15, bitrate=1000)
        print("Done!")
    except:
        print("probably need to install ffmpeg or some encoders")

if __name__ == '__main__':
    main()
