import matplotlib.pyplot as plt
import networkx as nx
import random
import collections
import math
from scipy.special import comb


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

def draw_bar(degrees, probabilites):
    plt.bar(degrees, probabilites, width=0.80, color='b')
    plt.gca().set_xlabel("Degree")
    plt.gca().set_ylabel("Binomial P(K)")
    plt.show()


def draw_theoretical_degree_distribution(g,p):
    degree_sequence = sorted([d for n, d in g.degree()], reverse=True)
    n = len(g)
    probabilities_list = list()
    for degree in degree_sequence:
        probabilities_list.append(comb(n-1,degree)
                                  *(math.pow(p,degree))
                                  *(math.pow(1-p,(n-1-degree))))
    draw_bar(degree_sequence,probabilities_list)


def main():
    n = int(raw_input('Enter the number of nodes '))
    p = float(raw_input('Enter the probability '))
    graph = create_graph(n)
    generate_erdos_renyi(graph, p)
    draw_graph(graph)
    draw_theoretical_degree_distribution(graph,p)


main()





