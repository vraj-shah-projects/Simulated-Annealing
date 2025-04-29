# libraries and setup
import networkx as nx
from numpy import sqrt, exp
from matplotlib import pyplot as plt, animation
from random import randint, choice, uniform
cities = nx.Graph()

fig = plt.figure()

# variables
no_of_cities = 5
nodes = []
edges = []
positions = {}
distances = {}
c = 0.1
t = 0

# temperature cooling function
def temperature(time):
    return 50*exp(-c*time)

def setup_graph(graph):
    # positions of cities
    for city in range(1,no_of_cities+1):
        graph.add_node(city)
        nodes.append(city)
        positions[city] = (randint(0,50),randint(0,50))

    # calculate distances for each edge
    for city in range(1,no_of_cities+1):
        for destination in range(1,no_of_cities+1):
            if city != destination:
                distance = round(sqrt((positions[destination][0]-positions[city][0])**2 + (positions[destination][1]-positions[city][1])**2),2)
                distances[(city,destination)] = distance

    # generate initial solution
    generate_from_path(cities,nodes,simulate_from_path(nodes))

# convert node path to list of edges
def simulate_from_path(path):
    edges = []
    for i in range(len(path)-1):
        edges.append((path[i],path[i+1]))
    edges.append((path[-1],path[0]))
    return edges

# generate edges on graph from node path 
def generate_from_path(graph,path,edges):
    global nodes
    nodes = path
    graph.remove_edges_from(list(graph.edges()))
    graph.add_edges_from(edges)

# calculate length of path from a given set of edges 
def path_length(edges):
    total = 0
    for edge in edges:
        total += distances[edge]
    return round(total,2)

# slightly adjust the solution by swapping two cities
def random_swap():
    new_path = nodes
    city_1 = randint(0,no_of_cities-1)
    city_2 = choice([i for i in range(no_of_cities) if i != city_1])

    new_path[city_1], new_path[city_2] = new_path[city_2], new_path[city_1]
    return {'path':new_path, 'edges':simulate_from_path(new_path)}

# main loop for simulated annealing
def animate(frame):
    fig.clear()
    global t

    current_case = cities.edges()
    test_case = random_swap()

    energy_current = path_length(current_case)
    energy_new = path_length(test_case['edges'])
    delta_energy = energy_new - energy_current

    if delta_energy < 0:
        generate_from_path(cities, test_case['path'],test_case['edges'])
    else:
        if exp(-delta_energy/temperature(t)) > uniform(0,1):
            generate_from_path(cities, test_case['path'],test_case['edges'])

    t += 1
    nx.draw(cities, node_color="red",pos=positions)

setup_graph(cities)

ani = animation.FuncAnimation(fig,animate,frames=6,interval=100,repeat=True)
plt.show()



