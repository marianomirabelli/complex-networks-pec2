from __future__ import division
import matplotlib.pyplot as plt
import networkx as nx
import random



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
    half_k = k/2
    connection_constant = (n - k/2)

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
    draw_graph(graph)

def main():
    while(True):
        nodes = int(raw_input('Enter the number of nodes '))
        k = int(raw_input('Enter the number of edges per nodes '))
        p = float(raw_input('Enter the probability'))
        generate_watts_strogatz(nodes,k,p)
        nx.watts_strogatz_graph

main()






