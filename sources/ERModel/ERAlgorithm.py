import matplotlib.pyplot as plt
import networkx as nx
import random


def draw_graph(g):
    layout = nx.circular_layout(g)
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


def main():
    n = int(raw_input('Enter the number of nodes'))
    p = float(raw_input('Enter the probability'))
    disconnected_graph = create_graph(n)
    generate_erdos_renyi(disconnected_graph, p)
    draw_graph(disconnected_graph)


main()





