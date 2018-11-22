#!/bin/python3

import math
import os
import random
import re
import sys
from functools import reduce
import operator


# Complete the findShortest function below.

#
# For the weighted graph, <name>:
#
# 1. The number of nodes is <name>_nodes.
# 2. The number of edges is <name>_edges.
# 3. An edge exists between <name>_from[i] to <name>_to[i].
#
#

def remove_parents(parents, successors):
    for index, value in enumerate(parents):
        print("successors[index]", successors[index], parents[index])
        successors[index] = [val for val in successors[index] if val is not value]
    return successors


def findShortest(graph_nodes, graph_from, graph_to, ids, val):
    distance = 0
    vertices_with_color_val = [index + 1 for index, value in enumerate(ids) if value is val]
    number_of_val_nodes = len(vertices_with_color_val)

    # if there are less than 2 color nodes then return immediately
    if number_of_val_nodes < 2:
        return -1

    # construct adjacency list
    adjacency_list = dict()
    number_of_edges = len(graph_from)
    for i in range(number_of_edges):
        a_node = graph_from[i]
        another_node = graph_to[i]
        if a_node in adjacency_list:
            adjacent_nodes = adjacency_list[a_node]
            adjacent_nodes.append(another_node)
            adjacency_list[a_node] = adjacent_nodes
        else:
            adjacent_nodes = []
            adjacent_nodes.append(another_node)
            adjacency_list[a_node] = adjacent_nodes

        if another_node in adjacency_list:
            adjacent_nodes = adjacency_list[another_node]
            adjacent_nodes.append(a_node)
            adjacency_list[another_node] = adjacent_nodes
        else:
            adjacent_nodes = []
            adjacent_nodes.append(a_node)
            adjacency_list[another_node] = adjacent_nodes

    # nodes having the given color
    vertices_to_check = vertices_with_color_val

    # maintain information about parents to discourage back tracking
    parents = []
    for _ in range(number_of_edges):
        next_nodes = [adjacency_list[node] for node in vertices_to_check]
        if parents:
            next_nodes = remove_parents(parents, next_nodes)
        parents = [[vertices_to_check[index]] * len(sublist) for index, sublist in enumerate(next_nodes)]

        # squeeze 2d list to 1d list
        next_nodes = reduce(operator.add, next_nodes)
        parents = reduce(operator.add, parents)

        distance += 1

        # if found then return
        for node in next_nodes:
            if node in vertices_with_color_val:
                return distance
        vertices_to_check = next_nodes

    # if no path exists then return 0
    return -1


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    graph_nodes, graph_edges = map(int, input().split())

    graph_from = [0] * graph_edges
    graph_to = [0] * graph_edges

    for i in range(graph_edges):
        graph_from[i], graph_to[i] = map(int, input().split())

    ids = list(map(int, input().rstrip().split()))

    val = int(input())

    ans = findShortest(graph_nodes, graph_from, graph_to, ids, val)

    fptr.write(str(ans) + '\n')

    fptr.close()
