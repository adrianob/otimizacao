import sys
import math
import copy
import random
import os
import numpy

if len(sys.argv) < 5:
    print("usage python sa.py <input_file> <temperature> <alpha> <neighbours>")
    exit()

file_in = open(sys.argv[1], "r")
temperature = float(sys.argv[2])
alpha = float(sys.argv[3])
neighbours = int(sys.argv[4])
lines = file_in.readlines()

dimension = int(lines[3].split(' ')[2])
capacity = int(lines[5].split(' ')[2])

node_coords = list(map(lambda line: map(lambda n: int(n), line.split(' ')[1:]), lines[7:(7+dimension)]))

#read demands of each node from input file
def read_demands():
    return list(map(lambda line: int(line.split(' ')[1]), lines[(7+dimension+1):(7+dimension+1+dimension)]))

k_min = int(math.ceil(sum(read_demands())/float(capacity)))

def generate_initial_solution():
    paths = []
    #generate random path for each truck that goes through all nodes
    for truck in xrange(0, k_min):
        path = [capacity]
        lst = [i for i in xrange(1,dimension)]
        for i in xrange(1,dimension):
            choice = random.choice(lst)
            lst.remove(choice)
            path.append(choice)
        paths.append(path)
    return paths

#clients in path have no demand
def no_more_demand(path, demands):
    over = True
    for city in path:
        if demands[city] != 0:
            over = False
    return over

#euclidian distance
def distance((x, y), (a, b)):
    return math.sqrt((x - a) ** 2 + (y - b) ** 2)

#all clients fullfiled their demands
def fullfiled_demand(demands):
    return all(v == 0 for v in demands)

def move_probability(delta, temperature):
    return math.exp((delta )/ temperature)

#return cost for given paths, remove unneded nodes from path
def test_paths(paths):
    temp_paths = copy.deepcopy(paths)
    cost = 0.0
    final_paths = []
    demands = read_demands()
    #each truck goes through its path until all demands are met
    for i in xrange(1, dimension):
        if fullfiled_demand(demands):
            break
        for path in temp_paths:
            if i <= len(path) - 1:
                city = path[i]
                if i == 1:
                    from_city = 0
                else:
                    from_city = path[i-1]
                cost = cost + distance(tuple(node_coords[from_city]), tuple(node_coords[city]))
                #has capacity
                if path[0] >= demands[city]:
                    path[0] = path[0] - demands[city]
                    demands[city] = 0
                else:
                    demands[city] = demands[city] - path[0]
                    path[0] = 0
                if path[0] == 0 or no_more_demand(path[i+1:], demands):
                    temp_paths.remove(path)
                    path = path[:i+1]
                    path[0] = capacity
                    final_paths.append(path)

    for path in temp_paths:
        path[0] = capacity
        final_paths.append(path)
    return cost, final_paths, demands

#shuffle two nodes in a path
def generate_candidate(paths):
    path = random.choice(paths)
    paths.remove(path)
    new_path = list(path)
    first_index = random.randrange(1, len(new_path))
    second_index = random.randrange(1, len(new_path))
    temp = new_path[first_index]
    new_path[first_index] = new_path[second_index]
    new_path[second_index] = temp
    paths.append(new_path)
    return paths

#main algorithm
def simulated_annealing():
    global temperature, alpha, neighbours

    new_demands = current_demands = read_demands()
    #create a viable initial solution
    while not fullfiled_demand(new_demands):
        current_paths = generate_initial_solution()
        current_cost, current_paths, new_demands = test_paths(list(current_paths))
    print "solucao inicial", current_cost
    while True:
        temperature = temperature * alpha
        if temperature < 0.1:
            return current_paths, current_cost
        for i in xrange(0, neighbours):
            temp = copy.deepcopy(current_paths)
            candidate = generate_candidate(temp)
            new_cost, new_paths, new_demands = test_paths(candidate)
            delta = current_cost - new_cost
            #better performance, chose as new starting point
            if delta > 0.0 and fullfiled_demand(new_demands):
                current_paths = copy.deepcopy(candidate)
                current_cost = new_cost
                current_demands = copy.deepcopy(new_demands)
            else:
                random_number = numpy.random.random()
                prob = move_probability(delta/100, temperature)
                #try to avoid max local
                if prob > random_number and fullfiled_demand(new_demands):
                    current_paths = copy.deepcopy(candidate)
                    current_demands = copy.deepcopy(new_demands)
                    current_cost = new_cost

paths, cost = simulated_annealing()
print "solucao final", cost, paths
