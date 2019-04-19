from __future__ import division
import collections
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import numpy as np
from scipy.special import comb


def div_d(my_dict,constant):

    for i in my_dict:
        my_dict[i] = float(my_dict[i]/constant)

    return my_dict

def draw_graph(g):
    layout = nx.random_layout(g)
    nx.draw_networkx(g, layout, False, False)
    plt.show()


def create_graph(n):
    graph = nx.Graph()
    graph.add_nodes_from(i for i in range(n))
    return graph


def generate_erdos_renyi(g,p):

    nodes = g.nodes()
    for i in nodes:
        for j in nodes:
            if(i!=j):
                r = random.random();
                if(r<=p and (not g.has_edge(j,i))):
                    g.add_edge(i,j)

def draw_empirical_bar(degrees, probabilites,probability_axis,color):
    plt.bar(degrees, probabilites, width=0.80, color=color)
    min_degree = min(degrees)
    max_degree = max(degrees)
    plt.xticks(np.arange(min_degree,max_degree,10))
    plt.xlim(min_degree, max_degree)
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel(probability_axis)
    plt.show()


def draw_theoretical_bar(degrees, probabilites,probability_axis,color):
    plt.bar(degrees, probabilites, width=0.80, color=color)
    min_degree = min(degrees)
    max_degree = max(degrees)
    plt.xticks(np.arange(min_degree,max_degree,2))
    plt.yticks(np.arange(0,0.15,0.01))
    plt.xlim(min_degree, max_degree)
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel(probability_axis)
    plt.show()


def draw_theoretical_degree_distribution(g,p):
    degree_sequence = sorted(set([d for n, d in g.degree()]))
    n = len(g)
    poisson_probabilities_list = list()
    binomial_probabilities_list = list()
    for degree in degree_sequence:
        binomial_probability =comb(n-1,degree)*(math.pow(p,degree))*(math.pow(1-p,(n-1-degree)))
        poisson_probability = (math.pow(n*p,degree) * math.pow(math.e,-(n*p))/math.factorial(degree))
        poisson_probabilities_list.append(poisson_probability)
        binomial_probabilities_list.append(binomial_probability)

    draw_theoretical_bar(degree_sequence,binomial_probabilities_list,'Binomial P(K)','b')
    draw_theoretical_bar(degree_sequence,poisson_probabilities_list,'Poisson  P(K)','r')

def draw_empirical_degree_distribution(g):
    degree_sequence = sorted(list([d for n, d in g.degree()]))
    n = len(g)
    degree_fec_tuple = collections.Counter(degree_sequence)
    degree_fec_tuple = div_d(degree_fec_tuple,float(n))
    degree, probabilities = zip(*degree_fec_tuple.items())
    draw_empirical_bar(degree,probabilities,'P(K)','g')


def main():
    n = int(raw_input('Enter the number of nodes '))
    p = float(raw_input('Enter the probability '))
    graph = create_graph(n)
    generate_erdos_renyi(graph, p)
    #draw_graph(graph)
    draw_theoretical_degree_distribution(graph,p)
    draw_empirical_degree_distribution(graph)


main()





