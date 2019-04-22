from __future__ import division
import collections
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import numpy as np


def get_index_range(index, length):
  trim = index % length;
  nonNegative = trim + length;
  return nonNegative % length;

def draw_graph(g):
    layout = nx.circular_layout(g)
    nx.draw_networkx(g, layout, False, False)
    plt.show()

def generate_watts_strogatz(n,k,p):
    if k > n:
        raise ValueError('The k value can not be greater than n')
    graph = nx.Graph()
    graph.add_nodes_from(i for i in range(n))
    nodes = graph.nodes()
    connection_constant = k/2
    for i in nodes:

        clockwise_index = 0
        while(clockwise_index < connection_constant):
            index = get_index_range(i + clockwise_index, n)
            if(i!=index):
                if(not(graph.has_edge(i,index)) and
                    not(graph.has_edge(index,i))):
                        graph.add_edge(i,index)
            clockwise_index += 1

        counter_clockwise_index = 0
        while(counter_clockwise_index < connection_constant):
            index = get_index_range(i - clockwise_index, n)
            if (i != index):
                if (not (graph.has_edge(i, index)) and
                        not (graph.has_edge(index, i))):
                    graph.add_edge(i, index)
            counter_clockwise_index+=1

    draw_graph(graph)

def main():
    while(True):
        nodes = int(raw_input('Enter the number of nodes '))
        k = int(raw_input('Enter the number of edges per nodes '))
        p = float(raw_input('Enter the probability'))
        generate_watts_strogatz(nodes,k,p)


main()






