from __future__ import division
import math
import collections
import operator
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt



class BinRange:

    def __init__(self,min,max):
        self.min = min
        self.max = max

    def __getitem__(self, item):
        return getattr(self, item)

    def __cmp__(self, other):
        return cmp(self.min, other.min)

def div_d(my_dict,constant):

    for i in my_dict:
        my_dict[i] = float(my_dict[i]/constant)

    return my_dict

def draw_graph(g,n,seed_nodes,edges_per_node):
    layout = nx.random_layout(g)
    nx.draw_networkx(g, layout, False, False)
    plt.savefig("results/ba_graph_"+str(n)+"_"+str(seed_nodes)+"_"+str(edges_per_node)+".png")
    plt.show()

def draw_log_scale_empirical_degree_distribution(degree_sequence,nodes,seed_nodes,edges_per_node):

    #Find max and min from K
    min_degree = min(degree_sequence)
    max_degree = max(degree_sequence)
    log_min_degree = np.log(min_degree)
    log_max_degree = np.log(max_degree+1)

    #Find logarithm for all degrees
    log_degree_sequence = list()
    for degree in degree_sequence:
        log_degree_sequence.append(np.log(degree))

    #Divide the interval log_min_degree - log_max_degree in bines
    bin_divider = (log_max_degree - log_min_degree)/10
    current_min_limit = log_min_degree
    log_bins = collections.OrderedDict()
    log_bin_degree_list = collections.OrderedDict()

    while(current_min_limit<log_max_degree):
        log_bins[current_min_limit]=0
        log_bin_degree_list[current_min_limit] = list()
        current_min_limit +=bin_divider
    log_bins[current_min_limit]=0
    log_bin_degree_list[current_min_limit] = list()

    #Count how many elements of log(k) has into a specific bin
    for degree in log_degree_sequence:
        bines = iter(log_bins.keys())
        current_min = bines.next()
        has_next = True
        while(has_next):
            try:
                current_max = bines.next()
                if(current_min <= degree < current_max):
                    log_bins[current_min]+=1
                    break
                current_min = current_max
            except StopIteration:
                has_next= False

    #Divide the numbers of element by bin by the graph size
    probability_list = list()
    degree_distribution = list()
    for bin in log_bins:
            degree_distribution.append(bin)
            probability_list.append(log_bins[bin]/nodes)

    plt.bar(degree_distribution, probability_list, width=bin_divider, color='r')
    plt.yticks(np.arange(0, 1, 0.10))
    plt.xticks(np.arange(log_min_degree, log_max_degree, bin_divider))
    plt.xlim(log_min_degree, log_max_degree)
    plt.gca().set_xlabel("Log Scale Degree")
    plt.gca().set_ylabel("P(K)")
    plt.savefig("results/ba_log_empirical_"+str(nodes)+"_"+str(seed_nodes)+"_"+str(edges_per_node)+".png")
    plt.show()


def draw_empirical_degree_distribution(degree_sequence,n,seed_nodes,edges_per_node):
    degree_fec_tuple = collections.Counter(degree_sequence)
    degree_fec_tuple = div_d(degree_fec_tuple,float(n))
    degree, probabilities = zip(*degree_fec_tuple.items())
    plt.bar(degree, probabilities, width=0.80, color='b')
    min_degree = min(degree)
    max_degree = max(degree)
    plt.xticks(np.arange(min_degree, max_degree, 20))
    plt.xlim(min_degree, max_degree)
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel('P(X)')
    plt.savefig("results/ba_empirical_"+str(n)+"_"+str(seed_nodes)+"_"+str(edges_per_node)+".png")
    plt.show()




def calculate_distribution_empirical_exponent(degree_sequence,nodes):
    min_degree = min(degree_sequence)
    sum = 0
    for degree in degree_sequence:
        sum += np.log((degree)/(min_degree-0.5))
    exponent = 1 + nodes*(math.pow(sum,-1))
    return exponent

def draw_theoretical_distribution(degree_sequence,n,seed_nodes,edges_per_node):
    probability_list = list()
    degree_list = list()
    for degree in set(degree_sequence):
        degree_list.append(degree)
        probability_list.append(math.pow(degree,-3))
    plt.bar(degree_list, probability_list, width=0.80, color='y')
    min_degree = min(degree_sequence)
    max_degree = max(degree_sequence)
    plt.xticks(np.arange(min_degree, max_degree, 5))
    plt.xlim(min_degree, max_degree)
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel('P(X)')
    plt.savefig("results/ba_theoretical_"+str(n)+"_"+str(seed_nodes)+"_"+str(edges_per_node)+".png")
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
    while(True):
        nodes = int(raw_input('Enter the number of nodes '))
        seed_nodes = int(raw_input('Enter the number of initial nodes '))
        edges_per_node = int(raw_input('Enter the number of edges per node '))
        graph = generate_barbasi_albert(nodes,seed_nodes,edges_per_node)
        degree_sequence = sorted(list([d for n, d in graph.degree()]))
        draw_graph(graph,nodes,seed_nodes,edges_per_node)
        draw_theoretical_distribution(degree_sequence,nodes,seed_nodes,edges_per_node)
        draw_log_scale_empirical_degree_distribution(degree_sequence,len(graph),seed_nodes,edges_per_node)
        draw_empirical_degree_distribution(degree_sequence,len(graph),seed_nodes,edges_per_node)
        nx.write_pajek(graph,"results/ba_graph_"+str(n)+"_"+str(seed_nodes)+"_"+str(edges_per_node)+".net")
        print ('Empirical Distribution Exponent :',calculate_distribution_empirical_exponent(degree_sequence,len(graph)))

main()