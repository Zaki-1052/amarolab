#!/usr/bin/python

'''
Generates a grid-like graph in matrix format containing the number of nodes
as specified in the input. The edges are given random values

Usage:
python graphmaker.py <N> # where N is the number of vertices in the graph

graph format:

<N> <start vertex> <target vertex>
<matrix containing edge weights>
'''

import sys, time, random
from math import sqrt, ceil
MAXWEIGHT = 10
MINWEIGHT = 0

N = int(sys.argv[1])
root = int(ceil(sqrt(N)))


print "%d\t%d\t%d" % (N, 1, N)

for i in range(N):
    # every node is connected to the node immediately to its right and left, above and below
    connections = []
    if i % root != 0: # if there are nodes on the left
        connections.append(i-1)
    if i % root != root - 1 and i != N-1: # if there is a node on the left
        connections.append(i+1)
    if i >= root: # then make a connection with the one above
        connections.append(i-root)
    if i < N-root: # then make a connection with the one below
        connections.append(i+root)
    #print "Node %d connections: " % i, connections
    row = [str(i)]
    for f in range(N): # for every column in this row

        if f in connections: # generate a random value for this edge
            weight = (random.random() * (MAXWEIGHT - MINWEIGHT))  + MINWEIGHT
            row.append("%6.6f" % weight)
        else:
            row.append("inf")

    print "\t".join(row)
