#importing
import networkx as nx
import scipy
import matplotlib.pyplot as plt

#making demo from review article, boolean type

#works
def get_nodes():
    number_nodes = 0
    nodes_initial = {}
    nodes = input("enter number nodes: ")
    for i in range(nodes):
        name = raw_input('enter node name:' )
        print name
        nodes_initial[name] = 0
    return nodes_initial

#works
def get_edges(nodes_initial):
    for key in nodes_initial:
        buddies = []
        print key
        number_of_buddies = input('How many positive edges out of this node? ')
        for i in range(number_of_buddies):
            buddies.append(raw_input('Name of node edge points to: '))
        nodes_initial[key] = buddies

#works
def main_menu():
    input_choice = 0
    print ('Run previous model: 1')
    print ('Make new model: 2')
    print ('Run simulation: 3')
    input_choice = input( 'Enter choice: ')
    return input_choice

#making graph intially
def translate_to_graph(nodes):
    graph = nx.DiGraph()
    hold_keys = []
    number_edges_out = 0
    for key in nodes:
        hold_keys.append(key)
        print 'this is the graph function', key
    graph.add_nodes_from(hold_keys)
    return graph








#making truth tables to keep while running simulations
def translate_to_tables():
    y = 1

a = get_nodes()
b = get_edges(a)
graph_attempt = translate_to_graph(a)
nx.draw(graph_attempt)
plt.show()
