import sys
import math
import random
import os

if len(sys.argv) < 2:
    print("usage python sa.py <input_file>")
    exit()

file_in = open(sys.argv[1], "r")
lines = file_in.readlines()

dimension = int(lines[3].split(' ')[2])
capacity = int(lines[5].split(' ')[2])
k_min = 3

node_coords = list(map(lambda line: map(lambda n: int(n), line.split(' ')[1:]), lines[7:(7+dimension)]))
demands = list(map(lambda line: int(line.split(' ')[1]), lines[(7+dimension+1):(7+dimension+1+dimension)]))

def generate_initial_solution():
    paths = []
    #generate random path for each truck
    for truck in xrange(0, k_min):
        path = [capacity]
        lst = [i for i in xrange(1,dimension)]
        for i in xrange(1,dimension):
            choice = random.choice(lst)
            lst.remove(choice)
            path.append(choice)
        paths.append(path)
    return paths

def no_more_demand(path):
    over = True
    for city in path:
        if demands[city] != 0:
            over = False
    return over

def distance((x, y), (a, b)):
    return math.sqrt((x - a) ** 2 + (y - b) ** 2)

def fullfiled_demand():
    return all(v == 0 for v in demands)

def test_paths(paths):
    cost = 0.0
    final_paths = []
    #each truck goes through its path until all demands are met
    for i in xrange(1, dimension):
        if fullfiled_demand():
            break
        for path in paths:
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
            if path[0] == 0 or no_more_demand(path[i+1:]):
                paths.remove(path)
                path = path[:i+1]
                final_paths.append(path)

    for path in paths:
        final_paths.append(path)
    return cost, final_paths

paths = generate_initial_solution()
cost, final_paths = test_paths(paths)

#add remaining paths
if fullfiled_demand():
    print 'achou'
    print cost
    for path in final_paths:
        print path

