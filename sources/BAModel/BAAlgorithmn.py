from __future__ import division
import operator
import networkx as nx
import random
import matplotlib.pyplot as plt



class BinRange:

    def __init__(self,min,max):
        self.min = min
        self.max = max

    def __getitem__(self, item):
        return getattr(self, item)

    def __cmp__(self, other):
        return cmp(self.min, other.min)


def draw_graph(g):
    layout = nx.random_layout(g)
    nx.draw_networkx(g, layout, False, False)
    plt.show()




def generate_barbasi_albert(N, seed_nodes, edges_per_new_node):

    if seed_nodes > N:
        raise ValueError('The initial nodes seed can not be greater than the total nodes N')
    if edges_per_new_node > seed_nodes:
        raise ValueError('The edges per new node can not be greater than seed_nodes')

    graph = nx.Graph()
    graph.add_nodes_from(i for i in range(seed_nodes))
    nodes = graph.nodes()
    total_nodes = graph.number_of_nodes()
    for i in nodes:
        for j in nodes:
            if (i != j):
                if (not graph.has_edge(j, i)):
                    graph.add_edge(i, j)

    while(graph.number_of_nodes() < N):

        generated_edges = 0
        current_new_node = total_nodes
        total_nodes += 1
        degrees_list = graph.degree()
        degree_sumatory = sum(d for n, d in degrees_list)
        bin_map = dict()
        current_min = 0.0

        for node, degree in degrees_list:
            aux_max_bin = current_min + degree
            bin_map[node] = BinRange(current_min, aux_max_bin)
            current_min = aux_max_bin

        sorted_bin_map = sorted(bin_map.items(), key=operator.itemgetter(1))
        graph.add_node(current_new_node)

        while(generated_edges < edges_per_new_node):

            probability = random.random() * degree_sumatory

            for node, bin_range in sorted_bin_map:

                if (bin_range.min <= probability < bin_range.max ):

                    if(not(graph.has_edge(current_new_node,node))):

                        generated_edges = generated_edges + 1
                        graph.add_edge(current_new_node,node)
                        break
    return graph



def main():
    nodes = int(raw_input('Enter the number of nodes '))
    seed_nodes = int(raw_input('Enter the number of nodes '))
    edges_per_node = int(raw_input('Enter the number of edges per node '))
    graph = generate_barbasi_albert(nodes,seed_nodes,edges_per_node)
    draw_graph(graph)

main()