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

def draw_graph(g,n,p):
    layout = nx.random_layout(g)
    nx.draw_networkx(g, layout, False, False)
    plt.savefig("results/er_graph_"+str(n)+"_"+str(p)+".png")
    plt.show()


def generate_erdos_renyi(n,p):
    graph = nx.Graph()
    graph.add_nodes_from(i for i in range(n))
    nodes = graph.nodes()
    for i in nodes:
        for j in nodes:
            if(i!=j):
                r = random.random();
                if(r<p and (not graph.has_edge(j,i))):
                    graph.add_edge(i,j)
    return graph


def draw_empirical_bar(n,p,degrees, probabilites,probability_axis,color):
    plt.bar(degrees, probabilites, width=0.80, color=color)
    min_degree = min(degrees)
    max_degree = max(degrees)
    plt.xticks(np.arange(min_degree,max_degree,3))
    plt.xlim(min_degree, max_degree)
    plt.ylim(0,1)
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel(probability_axis)
    plt.savefig("results/er_empirical_"+str(n)+"_"+str(p)+".png")
    plt.show()


def draw_theoretical_bar(n,p,type,degrees, probabilites,probability_axis,color):
    plt.bar(degrees, probabilites, width=0.80, color=color)
    min_degree = min(degrees)
    max_degree = max(degrees)
    plt.xticks(np.arange(min_degree,max_degree,3))
    plt.xlim(min_degree, max_degree)
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel(probability_axis)
    plt.savefig("results/er_theoretical_"+type+"_"+str(n)+"_"+str(p)+".png")
    plt.show()


def draw_theoretical_degree_distribution(g,p):
    degree_sequence = sorted(set([d for n, d in g.degree()]))
    n = len(g)
    degree_list = list()
    poisson_probabilities_list = list()
    binomial_probabilities_list = list()

    for degree in degree_sequence:

        binomial_probability =comb(n-1,degree)*(p**degree)*((1-p)**(n-1-degree))

        poisson_probability = (math.pow(n*p,degree) * math.pow(math.e,-(n*p))/math.factorial(degree))

        degree_list.append(degree)
        poisson_probabilities_list.append(poisson_probability)
        binomial_probabilities_list.append(binomial_probability)

    draw_theoretical_bar(n,p,"binomial",degree_list,binomial_probabilities_list,'Binomial P(K)','b')
    draw_theoretical_bar(n,p,"poisson",degree_list,poisson_probabilities_list,'Poisson  P(K)','r')

def draw_empirical_degree_distribution(g,p):
    degree_sequence = sorted(list([d for n, d in g.degree()]))
    n = len(g)
    degree_fec_tuple = collections.Counter(degree_sequence)
    degree_fec_tuple = div_d(degree_fec_tuple,float(n))
    degree, probabilities = zip(*degree_fec_tuple.items())
    draw_empirical_bar(n,p,degree,probabilities,'P(K)','g')


def main():
    while(True):
        n = int(raw_input('Enter the number of nodes '))
        p = float(raw_input('Enter the probability '))
        graph = generate_erdos_renyi(n, p)
        draw_graph(graph,n,p)
        draw_theoretical_degree_distribution(graph,p)
        draw_empirical_degree_distribution(graph,p)
        nx.write_pajek(graph,"results/er_graph_"+str(n)+"_"+str(p)+".net")

main()





