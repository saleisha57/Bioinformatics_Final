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
#added directions (inhibition, not inhibition) based on +/- on back as can only do -> and not -| edges wtih networkx
def get_edges(nodes_initial):
    for key in nodes_initial:
        buddies = []
        print key
        number_of_buddies = input('How many edges out of this node? ')
        for i in range(number_of_buddies):
            hold_friend = raw_input('Name of node edge points to: ')
            hold_direction = raw_input('Enter if +/- edge: ')
            hold_friend = hold_friend + hold_direction
            buddies.append(hold_friend)
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
#need to figure out how to do self-edges, change negative edges into a different color so as to differentiate between directions
#maybe negative strength values in networkx directed mode?
def translate_to_graph(nodes):
    graph = nx.DiGraph()
    hold_keys = []
    number_edges_out = 0
    for key in nodes:
        hold_keys.append(key)
    graph.add_nodes_from(hold_keys)
    for key in nodes:
        for sub_key in nodes[key]:
            graph.add_edge(key,sub_key[0:len(sub_key) - 1])
    return graph


#making truth tables to keep while running simulations
def translate_to_tables(nodes):
    all_tables = {}
    for key in nodes:
        all_tables[key] = make_a_truth_table(key)
    return all_tables

#gets all the nodes which point to a given node
#need to build networkx graph first
def roll_call(nodes, search_node):
    give_back_list_friends=[]
    print search_node
    for thing in nodes:
        print 'in first for', thing
        for thing_2 in nodes[thing]:
            print 'in second for', thing_2
            if search_node == thing_2[0:len(thing_2) - 1]:
                give_back_list_friends.append(thing + thing_2[len(thing_2)-1:len(thing_2)])
    return give_back_list_friends


#function to make a single truth table for a key
def make_truth_tables(nodes):
    tables={}
    #gets all nodes which point to a node, and +/- sign
    for thing in nodes:
        tables[thing] = roll_call(nodes, thing)
    return tables

def get_logic_rule(nodes_sorted, key):
    print "Enter Node", key, 'Logic:'
    print "nodes which point to ", key, 'and +/-:'
    for thing in nodes_sorted[key]:
        print thing[0:len(thing)-1], " ", thing[len(thing)-1:len(thing)]
    logic_uncut = raw_input("Enter logic function for ", key, " (using ~, (), OR, AND for then statement of if->then statement)")
    shakedown = cut_logic(logic_uncut)
    return shakedown

def cut_logic(logic_statement):
    



#a = get_nodes()
#b = get_edges(a)
#graph_attempt = translate_to_graph(a)
a = {'a': ['b+', 'c-'], 'b': ['a+'], 'c': ['b+']}
print a
print 'truth tables', make_truth_tables(a)
#nx.draw(graph_attempt)
#plt.show()
