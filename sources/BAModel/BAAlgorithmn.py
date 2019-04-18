import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(g):
    layout = nx.circular_layout(g)
    nx.draw_networkx(g, layout, False, False)
    plt.show()


def generate_barbasi_albert(N,m0,m):

    if m0>N:
        raise ValueError('The initial nodes seed can not be greater than the total nodes N')
    graph = nx.Graph()
    graph.add_nodes_from(i for i in range(m0))
    current_node = 0
    while(current_node < m0-1):
        next_node = current_node+1
        graph.add_edge(current_node,next_node)
        current_node = next_node
    graph.add_edge(current_node,0)
    return graph


generatedGraph = generate_barbasi_albert(100,5,3)
draw_graph(generatedGraph)
