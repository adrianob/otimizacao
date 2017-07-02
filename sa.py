import sys
import math
import copy
import random
import os
import numpy

if len(sys.argv) < 2:
    print("usage python sa.py <input_file>")
    exit()

file_in = open(sys.argv[1], "r")
lines = file_in.readlines()

dimension = int(lines[3].split(' ')[2])
capacity = int(lines[5].split(' ')[2])

node_coords = list(map(lambda line: map(lambda n: int(n), line.split(' ')[1 if line[0] == ' ' else 0:]), lines[7:(7+dimension)]))


#read demands of each node from input file
def read_prizes():
    return list(map(lambda line: int(line.split(' ')[1]), lines[(7+dimension+1):(7+dimension+1+dimension)]))


# print node_coords
prizes = read_prizes()

#choose randomly 1/2 the cities
def generate_initial_solution():
    coords = copy.deepcopy(node_coords)
    path = []
    path.append(coords[0])
    coords = coords[1:]
    random.shuffle(coords)
    path.extend(coords[0:len(coords)/2])
    path.append(node_coords[0])
    return path


# euclidian distance
def distance((x, y), (a, b)):
    return math.sqrt((x - a) ** 2 + (y - b) ** 2)

# shuffle two nodes in a path
def path_shuffle(paths):
    if len(paths) < 4:
        return paths
    i = random.randrange(1, len(paths)-1)
    j = i - 1 if (i == len(paths)-2) else i + 1
    paths[i], paths[j] = paths[j], paths[i]
    return paths

# 2-opt
def twoopt(paths):
    if len(paths) <= 4:
        return paths
    i = random.randrange(1, len(paths)/2)
    k = random.randrange(len(paths)/2 + 1, len(paths) - 1)
    new_route = paths[0:i]
    new_route.extend(reversed(paths[i:k + 1]))
    new_route.extend(paths[k+1:])
    return new_route

def cost(path):
    total_cost = 0
    dist = 0
    for i,city in enumerate(path[0:len(path)-1]):
        dist += distance((city[1], city[2]), (path[i+1][1], path[i+1][2]))
        total_cost += dist
        prize = prizes[city[0]-1]
        total_cost -= prize
    return total_cost


def generate_neighbours(path):
    choice = random.randrange(1, 6)
    new_path = copy.deepcopy(path)

    #shuffle 2 nodes
    if choice == 1:
        new_path = path_shuffle(path)
    #add node not in path
    elif choice == 2 and len(new_path) < len(node_coords):
        diff = []
        for node in node_coords:
            found = False
            for p in new_path:
                if p[0] == node[0]:
                    found = True
            if not found:
                diff.append(node)

        random.shuffle(diff)
        index = random.randrange(1, len(new_path)-1)
        new_path.insert(index, diff[0])
    #remove node from path
    elif len(new_path) > 3 and choice == 3:
        index = random.randrange(1, len(new_path)-1)
        new_path.pop(index)
    #2-opt
    elif len(new_path) > 3 and choice == 4:
        new_path = twoopt(path)
    #replace node with one not in path
    elif choice == 5 and len(new_path) < len(node_coords):
        diff = []
        for node in node_coords:
            found = False
            for p in new_path:
                if p[0] == node[0]:
                    found = True
            if not found:
                diff.append(node)

        random.shuffle(diff)
        index = random.randrange(1, len(new_path)-1)
        new_path.pop(index)
        new_path.insert(index, diff[0])

    return new_path


def local_search(initial_path):
    runs = 0
    current = copy.deepcopy(initial_path)
    current_cost = cost(current)
    while runs < 10:
        runs += 1
        temp = copy.deepcopy(current)
        for i in xrange(0, 20):
            neighbour = generate_neighbours(temp)
            cost_n = cost(neighbour)
            if cost_n < current_cost:
                current_cost = cost_n
                current = copy.deepcopy(neighbour)

    return current


# cross exchange
def perturbation(path):
    paths = copy.deepcopy(path)
    if len(paths) > 11:
        i = 2
        i = random.randrange(2, len(paths)/4)
        paths[i], paths[i+2], paths[i+4], paths[i+6] = paths[i+6], paths[i], paths[i+2], paths[i+4]

    return paths


def ils():
    initial_path = generate_initial_solution()
    # print cost(initial_path)
    local_min = local_search(initial_path)
    min_cost = cost(local_min)
    # print min_cost
    runs = 0
    while runs < len(node_coords)/2:
        runs += 1
        temp2 = copy.deepcopy(local_min)
        per = perturbation(temp2)
        temp = copy.deepcopy(per)
        ls = local_search(temp)
        ls_cost = cost(ls)
        if ls_cost < min_cost:
            local_min = copy.deepcopy(ls)
            min_cost = ls_cost
    print min_cost
    print local_min

ils()
