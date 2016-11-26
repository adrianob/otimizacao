import sys
import os

if len(sys.argv) < 2:
  print("usage python sa.py <input_file>")
  exit()

file_in = open(sys.argv[1], "r")
lines = file_in.readlines()

dimension = int(lines[3].split(' ')[2])
capacity = int(lines[5].split(' ')[2])

node_coords = list(map(lambda line: map(lambda n: int(n), line.split(' ')[1:]), lines[7:(7+dimension)]))
demands = list(map(lambda line: int(line.split(' ')[1]), lines[(7+dimension+1):(7+dimension+1+dimension)]))

print dimension
print capacity
print node_coords
print demands
