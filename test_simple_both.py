#importing
import networkx as nx
import matplotlib.pyplot as plt
from truths import Truths
import itertools

#global variables for model
#still need:  nodes, buddies, etc that are all called multiple times
#maybe a 'model type' variable for truth table vs. sigma type update schemes
current_state = {}
past_states = {}
#list of node_names, in alphabetical order.  Store all in alphabetical order for generation values
node_names = []
#nodes as keys, edges as list elements
nodes = {}
#constants for sigma function updating
ar = 0
ag = 0
#stores a node as a key, with all nodes which have edges which connect to that node and their interactions in a list
key_with_partners = {}


#MODEL ENTRY functions
#node entry, user input of all node names
def get_nodes():
    names_store = []
    global node_names
    nodes_initial = {}
    nodes = input("enter number nodes: ")
    for i in range(nodes):
        name = raw_input('enter node name:' )
        print name
        names_store.append(name)
        nodes_initial[name] = []
    names_store.sort()
    node_names = names_store
    return nodes_initial

#added directions (inhibition, not inhibition) based on +/- on back as can only do -> and not -| edges wtih networkx
def get_edges():
    nodes_initial = get_nodes()
    global nodes
    for key in nodes_initial:
        buddies = []
        #print key
        number_of_buddies = input('How many edges out of this node? ')
        for i in range(number_of_buddies):
            hold_friend = raw_input('Name of node edge points to: ')
            hold_direction = raw_input('Enter if +/- edge: ')
            #putting direction at end of node name
            hold_friend = hold_friend + hold_direction
            buddies.append(hold_friend)
        nodes_initial[key] = buddies
    nodes = nodes_initial

#INITIAL SET UP FUNCTIONS
#makes a di_graph
def translate_to_graph():
    global nodes
    graph = nx.DiGraph()
    hold_keys = []
    number_edges_out = 0
    for key in nodes:
        hold_keys.append(key)
    graph.add_nodes_from(hold_keys)
    for key in nodes:
        for sub_key in nodes[key]:
            if sub_key[len(sub_key)-1:len(sub_key)] == '+':
                graph.add_edge(key,sub_key[0:len(sub_key) - 1], color = 'r')
            else:
                graph.add_edge(key,sub_key[0:len(sub_key) - 1], color = 'g')
    return graph

#PUT TRUTH TABLE MAKING HERE


#find all the nodes which point to a given node, saves interaction type
def find_all_nodes_with_point_to_a_node(search_node):
    global nodes
    global key_with_partners
    give_back_list_friends=[]
    #print search_node
    for thing in nodes:
        #print 'in first for', thing
        for thing_2 in nodes[thing]:
            #print 'in second for', thing_2
            if search_node == thing_2[0:len(thing_2) - 1]:
                give_back_list_friends.append(thing + thing_2[len(thing_2)-1:len(thing_2)])
    key_with_partners = give_back_list_friends

def retreive_model_value(key):
    return current_state[key]

#does a signma update scheme
def sigma_function_new_value(value_old):
    sum_val = 0
    global ar
    global ag
    global nodes
    global key_with_partners
    for thing in key_with_partners:
        if thing[len(thing) - 1:len(thing)] == '+':
            sum_val = sum_val + ag * retreive_model_value(thing[0:len(thing) -1])
        else:
            sum_val = sum_val + ar * retreive_model_value(thing[0:len(thing) - 1])
    if sum_val > 0:
        return_val = 1
    else if sum_val < 0:
        return_val = 0
    else:
        return_val = value_old
    return return_val

#runs a single generation update
def run_a_generation_sigma(ar_n, ag_g, nodes generaton_numb):
    ar_n = raw_input("Enter ar value: ")
    ag_n = raw_input("Enter ag value: ")
    global key_with_partners
    past_states[generaton_numb] = current_state
    current_value_store = 0
    #now update
    for thing in nodes:
        current_value_store = current_state[thing]
        current_state[thing] = sigma_function_new_value(ar, ag, nodes, key_with_partners, current_value_store)

def run_set_number_generations_sigma(number, ar, ag, nodes, key_with_partners, intial_values):
    current_state = initial_values
    for i in range(number):
        run_a_generation_sigma(ar, ag, nodes, key_with_partners, i)
    #need output stuff

#MENY AND FILE I/O STUFF
#works
def main_menu():
    input_choice = 0
    print ('Run previous model: 1')
    print ('Make new model: 2')
    print ('Run simulation: 3')
    input_choice = input( 'Enter choice: ')
    return input_choice

#takes input of graph
def draw_the_graph(y):
        edges = y.edges()
        pos = nx.circular_layout(y)
        colors = [y[u][v]['color'] for u,v in edges]
        nx.draw(y, pos, edges=edges, edge_color=colors, with_labels = True)

def split_node_history_and_graph(past_gen_data):
    domain = len(past_gen_data)
    dom = []
    broken_by_nodes = {}
    for i in range(domain):
        dom.append(i)
    global node_names
    for a in node_names:
        broken_by_nodes[a] = []
    print broken_by_nodes
    for thing in past_gen_data:
        print thing
        for a in range(len(past_gen_data[thing])):
            broken_by_nodes[node_names[a]].append(past_gen_data[thing][a])
    for b in range(len(node_names)):
        plt.figure(b)
        plt.plot(broken_by_nodes[node_names[b]])
        plt.title(node_names[b])
        name = node_names[b] + 'node_state_history'
        plt.savefig(name)
        plt.show()
        plt.close()

#UNFINISHED TRUTH TABLE STUFF
#making truth tables to keep while running simulations


#function to make a single truth table for a key
def make_truth_tables_rows(nodes):
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

#translate logic into piecewise 1 and 0 based functions?
def cut_logic(logic_statement):
    placeholder = 0

#gets all rows for table
#works
#handles expansions well
def get_table_rows(node_number):
    k = list(itertools.product([1,0], repeat = node_number))
    return k

#test stuff
a = {'a': ['b+', 'c-'], 'b': ['a-'], 'c': ['b+']}
y = translate_to_graph(a)
draw_the_graph(y)

plt.show()
print 'truth tables', make_truth_tables(a)
