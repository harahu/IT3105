import math, random
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# for animation
fig = plt.figure()
ax = plt.axes(xlim=(-0.2,1.2), ylim=(-0.2,1.2))
cities_plt, = ax.plot([], [], 'ro', zorder=2, alpha=0.4)
neurons_plt, = ax.plot([], [], 'yo-', zorder=1)
distance_text = ax.text(-0.1, -0.1, "", transform=ax.transAxes)

def get_problem_set(filename):
    """Returns a list of max-normalized city coordinates"""
    with open(filename, 'r') as f:
        inp = [line.rstrip('\n') for line in f]
    inp = inp[7:-2]

    for i in range(len(inp)):
        inp[i] = inp[i].split(' ')[1:]
        inp[i] = [float(j) for j in inp[i]]

    max_x = max(city[0] for city in inp)
    min_x = min(city[0] for city in inp)
    max_y = max(city[1] for city in inp)
    min_y = min(city[1] for city in inp)

    inp_norm = [[(city[0]-min_x)/(max_x-min_x), (city[1]-min_y)/(max_y-min_y)] for city in inp]

    return inp, inp_norm

def plot_som_tsp(cities, neurons):
    x0 = [city[0] for city in cities]
    y0 = [city[1] for city in cities]
    plt.plot(x0, y0, 'ro')
    x1 = [neuron[0] for neuron in neurons]
    y1 = [neuron[1] for neuron in neurons]
    x1.append(x1[0])
    y1.append(y1[0])

    plt.plot(x1, y1, 'yo-')
    plt.show()

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

def euclidian_distance(a, b):
    return math.sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))

def get_best_match_index(city, neuron_list):
    best = 0
    best_dist = 10

    for i in range(len(neuron_list)):
        distance = euclidian_distance(city, neuron_list[i])
        if distance < best_dist:
            best = i
            best_dist = distance
            
    return best

# Returns list of the closest cities per neuron
def get_closest_city_list(som_ring, cities):
    closest_list = [set() for i in range(len(som_ring))]
    
    # Add closest city to each neuron
    for neuron_index in range(len(som_ring)):
        closest_city = get_best_match_index(som_ring[neuron_index], cities)
        closest_list[neuron_index].add(closest_city)
    
    # Add closest neuron for each city (if more than one city has the same neuron as closest)
    for city_index in range(len(cities)):
        closest_neuron = get_best_match_index(cities[city_index], som_ring)
        closest_list[closest_neuron].add(city_index)
    
    return closest_list

def calculate_total_distance(som_ring, cities, raw_cities):
    total_distance = 0
    closest_list = [list(cty) for cty in get_closest_city_list(som_ring, cities)]
    
    processed_cities = [closest_list[0][0]]
    last_city = closest_list[0][0]
    for city_list in closest_list:
        for city in city_list:
            if city not in processed_cities:
                total_distance += euclidian_distance(raw_cities[city], raw_cities[last_city])
                last_city = city
    
    total_distance += euclidian_distance(raw_cities[processed_cities[0]], raw_cities[last_city])
    
    return total_distance
    
def train(weight, city, alpha, discount):
    weight[0] += alpha*discount*(city[0]-weight[0])
    weight[1] += alpha*discount*(city[1]-weight[1])

def main():
    #initialization
    tspfile = "wi29.tsp"
    raw_cities, cities = get_problem_set(tspfile)
    #som_ring = [[random.random() for i in range(2)] for i in range(len(cities))]
    som_ring = []
    for i in range(len(cities)*2):
        tetha = i / len(cities) * 2 * math.pi
        som_ring.append([math.cos(tetha)/2 + 0.5, math.sin(tetha)/2 + 0.5])
    eta = 0.8
    delta = 6.2 + 0.037*len(cities)
    n_iterations = 50*len(cities)
    frame_step = 30
    
    # for animation plot
    neurons_data = []
    distance_data = []
    add_anim(neurons_data, distance_data, som_ring, cities, raw_cities)
    
    for i in range(n_iterations):
        #city = random.choice(cities)
        city = cities[i%len(cities)]
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
        
        if i % frame_step == 0:
            add_anim(neurons_data, distance_data, som_ring, cities, raw_cities)
    
    #plot_som_tsp(cities, som_ring)
    
    init_anim(cities)
    ani = anim.FuncAnimation(fig, animate, frames=len(neurons_data), fargs=(neurons_data,distance_data,))
    
    try:
        ani.save("tsp_%s.mp4" %(tspfile), fps=15, bitrate=1000)
    except:
        print("probably need to install ffmpeg or some encoders")
    plt.show()

if __name__ == '__main__':
    main()
