from __future__ import division
import matplotlib.pyplot as plt
import networkx as nx
import collections
import random
import math
import numpy as np
from scipy.special import comb





def get_index_range(index, length):
  trim = index % length;
  nonNegative = trim + length;
  return nonNegative % length;

def draw_graph(g):
    layout = nx.circular_layout(g)
    nx.draw_networkx(g, layout, False, False)
    plt.show()

def div_d(my_dict,constant):

    for i in my_dict:
        my_dict[i] = float(my_dict[i]/constant)

    return my_dict

def draw_empirical_degree_distribution(degree_sequence,n):
    degree_fec_tuple = collections.Counter(degree_sequence)
    degree_fec_tuple = div_d(degree_fec_tuple,float(n))
    degree, probabilities = zip(*degree_fec_tuple.items())
    plt.bar(degree, probabilities, width=0.80, color='b')
    min_degree = min(degree)
    max_degree = max(degree)
    plt.xticks(np.arange(min_degree, max_degree, 1))
    plt.xlim(min_degree, max_degree)
    plt.ylim(0, 1)
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel('P(X)')
    plt.show()

def draw_theoretical_degree_distribution(degree_sequence,n,k,p):
    half_k = k/2
    degree_list = list()
    probability_list = list()
    for degree in set(degree_sequence):
        probability = 0
        index = 1
        min_value = min(degree-half_k,int(half_k))

        while(index<=min_value):
            degree_factor = degree - half_k - index
            probability+= comb(half_k,index) * math.pow(1-p,n) * math.pow(p,half_k-index) * \
                          (math.pow((p*k)/2,degree_factor))/(math.factorial(degree_factor))*math.exp(-p*half_k)
            index+=1
        degree_list.append(degree)
        probability_list.append(probability)

    plt.bar(degree_list, probability_list, width=0.80, color='y')
    min_degree = min(degree_sequence)
    max_degree = max(degree_sequence)
    plt.xticks(np.arange(min_degree, max_degree, 1))
    plt.xlim(min_degree, max_degree)
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel('P(X)')
    plt.show()


def generate_watts_strogatz(n,k,p):
    if k > n:
        raise ValueError('The k value can not be greater than n')
    if k % 2 !=0:
        raise ValueError('The k value must be even')

    graph = nx.Graph()
    graph.add_nodes_from(i for i in range(n))
    nodes = graph.nodes()
    half_k = k/2
    connection_constant = (n - half_k)

    for i in nodes:

       for j in nodes:

           current_index = abs(i - j)
           if 0 < current_index%connection_constant <= half_k:
                graph.add_edge(i,j)

    for i in nodes:

        for j in nodes:

                if(graph.has_edge (i,j) and (i < j <= i+half_k)):

                    current_probability = random.random()
                    if(current_probability<p):

                        if (not (graph.degree(i) >= n - 1)):
                           random_node = random.randint(0,n-1)
                           while i == random_node or graph.has_edge(i, random_node):
                             random_node = random.randint(0,n-1)

                           graph.remove_edge(i, j)
                           graph.add_edge(i, random_node)
                        else:
                            break
    return graph
def main():
    while(True):
        nodes = int(raw_input('Enter the number of nodes '))
        k = int(raw_input('Enter the number of edges per nodes '))
        p = float(raw_input('Enter the probability'))
        graph = generate_watts_strogatz(nodes,k,p)
        draw_graph(graph)
        degree_sequence = sorted(list([d for n, d in graph.degree()]))
        draw_empirical_degree_distribution(degree_sequence,nodes)
        draw_theoretical_degree_distribution(degree_sequence,nodes,k,p)
main()






