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
delta_text = ax.text(0.3, -0.1, "", transform=ax.transAxes)

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

    for city in inp:
        city.reverse()
    for city in inp_norm:
        city.reverse()

    return inp, inp_norm

def plot_som_tsp(cities, raw_cities, neurons, fname, cur_iter, max_iter):
    """Create and save plot of current state"""
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
    iter_text = ax2.text(0.3, -0.1, "Iteration: %i / %i" %(cur_iter, max_iter), transform=ax2.transAxes)
    plt.savefig("./plots/%s" %fname)
    plt.figure(1)

def init_anim(cities):
    """Initialize cities plot"""
    cities_plt.set_data([], [])
    
    x = [city[0] for city in cities]
    y = [city[1] for city in cities]
    cities_plt.set_data(x, y)

def animate(i, neurons, distances, deltas):
    """Create plot for frame i"""
    neurons_plt.set_data([], [])
    
    x = neurons[i][0]
    y = neurons[i][1]
    
    neurons_plt.set_data(x, y)
    distance_text.set_text("Distance: %0.4f" %(distances[i]))
    delta_text.set_text("Delta: %0.4f" %(deltas[i]))
    return cities_plt, neurons_plt, distance_text, delta_text

def add_anim(neurons_data, distance_data, delta_data, delta, neurons, cities, raw_cities):
    """Add frame to animation"""
    x = [neuron[0] for neuron in neurons]
    y = [neuron[1] for neuron in neurons]
    
    x.append(neurons[0][0])
    y.append(neurons[0][1])
    
    neurons_data.append((x,y))
    distance_data.append(calculate_total_distance(neurons, cities, raw_cities))
    delta_data.append(delta)

def print_diagnostics(i, n_iterations, eta, delta):
    print("Progress: %i%%" %(round(100*i/n_iterations)))
    print("Eta: %f" %(eta))
    print("Delta: %f" %(delta), end='\033[F\033[F')
    if i == n_iterations-1:
        print('\n\n\n----------')

def euclidian_distance(a, b):
    x = a[0]-b[0]
    y = a[1]-b[1]
    return math.sqrt((x*x)+(y*y))

def euclidian_potential(a, b):
    x = a[0]-b[0]
    y = a[1]-b[1]
    return (x*x)+(y*y)

def get_best_match_index(city, neurons, disregard):
    """Returns index of neuron not in disregard closest to city"""
    best = 0
    potential = []
    for n in neurons:
        potential.append(euclidian_potential(city, n))
    for d in disregard:
        potential[d] = 1000000000
    best_pot = potential[0]

    for i in range(1, len(neurons)):
        if potential[i] < best_pot:
            best = i
            best_pot = potential[i]
            
    return best

# Returns list of the closest cities per neuron
def get_closest_city_list(som_ring, cities):
    closest_list = [set() for i in range(len(som_ring))]
    
    # Add closest neuron for each city
    for city_index in range(len(cities)):
        closest_neuron = get_best_match_index(cities[city_index], som_ring, [])
        closest_list[closest_neuron].add(city_index)
    
    return closest_list

def calculate_total_distance(som_ring, cities, raw_cities):
    total_distance = 0
    closest_list = [list(cty) for cty in get_closest_city_list(som_ring, cities)]
    closest_list = [cty for cty in closest_list if len(cty) != 0]
    
    last_city = closest_list[0][0]
    for city_list in closest_list:
        for city in city_list:
            total_distance += euclidian_distance(raw_cities[city], raw_cities[last_city])
            last_city = city
    total_distance += euclidian_distance(raw_cities[closest_list[0][0]], raw_cities[last_city])
    
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
    tspfile = files[3]
    if len(sys.argv) > 1:
        tspfile = sys.argv[1]
    raw_cities, cities = get_problem_set(tspfile)
    som_ring = []
    pick_list = cities[:]
    inhibit = []
    n_neurons = int(len(cities)*1.5)
    
    # Create initial circular position of nodes
    for i in range(n_neurons):
        tetha = i / n_neurons * 2 * math.pi
        som_ring.append([math.cos(tetha)/3 + 0.5, math.sin(tetha)/3 + 0.5])
    
    # Init variables
    init_eta = 0.8 #learning rate
    init_delta = 6.2 + 0.037*len(som_ring) #neighbourhood radius
    if len(sys.argv) > 3:
        try:
            init_eta = float(sys.argv[3])
            init_delta = float(sys.argv[4])
        except ValueError:
            print("Usage: python tsp.py [file] [decay type] [learning rate] [initial delta]")
    eta = init_eta
    delta = init_delta
    n_iterations = 50*len(som_ring)
    
    # Set decay type
    decay_type = 1
    if len(sys.argv) > 2:
        try:
            decay_type = int(sys.argv[2])
        except ValueError:
            print("Usage: python tsp.py [file] [decay type] [learning rate] [initial delta]")
    frame_step = len(cities)
    
    # Variables used for animation plot
    neurons_data = []
    distance_data = []
    delta_data = []
    add_anim(neurons_data, distance_data, delta_data, delta, som_ring, cities, raw_cities)
    plot_som_tsp(cities, raw_cities, som_ring, "%s_%i_start.png" %(tspfile[5:-4], decay_type), 1, n_iterations)
    
    for i in range(n_iterations):
        if i % len(cities) == 0:
            #shuffles cities and clears inhibition for every pass through of the list
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
            eta = exponential_decay(init_eta, i, n_iterations/3)
            delta = exponential_decay(init_delta, i, n_iterations/3)
            if delta < 1:
                delta = 1

        #document
        if (i+1) % frame_step == 0:
            print_diagnostics(i, n_iterations, eta, delta)
            add_anim(neurons_data, distance_data, delta_data, delta, som_ring, cities, raw_cities)
        
        if i == int(n_iterations/2):
            plot_som_tsp(cities, raw_cities, som_ring, "%s_%i_middle.png" %(tspfile[5:-4], decay_type), i+1, n_iterations)
            pass

    plot_som_tsp(cities, raw_cities, som_ring, "%s_%i_end.png" %(tspfile[5:-4], decay_type), i+1, n_iterations)
    init_anim(cities)
    ani = anim.FuncAnimation(fig, animate, frames=len(neurons_data), fargs=(neurons_data,distance_data,delta_data,))
    
    print("Final distance: %.4f" %(distance_data[-1]))
    
    # Show animation and save video
    plt.show()
    try:
        print("Saving video...")
        ani.save("./animations/%s_%i.mp4" %(tspfile[5:-4], decay_type), fps=15, bitrate=1000)
        print("Done!")
    except:
        print("probably need to install ffmpeg or some encoders")

if __name__ == '__main__':
    main()
