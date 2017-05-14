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
def run_a_generation_sigma(generaton_numb):
    past_states[generaton_numb] = current_state
    current_value_store = 0
    #now update
    for thing in nodes:
        current_value_store = current_state[thing]
        current_state[thing] = sigma_function_new_value(current_value_store)

def run_set_number_generations_sigma(number, intial_values):
    current_state = initial_values
    for i in range(number):
        run_a_generation_sigma(i)
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


def open_old_model(name):
    full_name = name + '.txt'
    x = open(full_name)
    x_in = x.read()
    blank = []
    x_in_split = [s.strip() for s in x_in.splitlines()]
    for pos in range(len(x_in_split)):
        wordList = x_in_split[pos].split(" ")
        blank.append(wordList)
    return blank

def assign_all_things(read_stuff_list):
    #assigns main nodes, edges out of node
    global nodes
    global key_with_partners
    for thing in range(len(read_stuff_list[0])):
        nodes[read_stuff_list[0][thing]] = read_stuff_list[thing + 1]
        key_with_partners[read_stuff_list[0][thing]] = read_stuff_list[thing + len(read_stuff_list[0]) + 1]
    location_model_type = len(read_stuff_list[0]) * 2 + 1
    #print location_model_type
    model = read_stuff_list[1 + (len(read_stuff_list[0]) *2)][0]
    #print model
    global m_type
    m_type = model
    if m_type == 'sigma':
        global ag
        global ar
        location_model_type = location_model_type + 1
        ag = read_stuff_list[location_model_type][1]
        ar = read_stuff_list[location_model_type+1][1]
    else:
        placeholder = 0
        #figure out truth table export import once working
#prints a model to a text file, same format as in examples
def file_output_model(name):
    x = open(name+'.txt', 'w')
    global nodes
    global key_with_partners
    global m_type
    for thing in nodes:
        x.write( thing+ " ")
    x.write( "\n")
    for thing in nodes:
        for thing_2 in nodes[thing]:
            x.write( thing_2)
            x.write('\n')
    for thing in key_with_partners:
        for thing_2 in key_with_partners[thing]:
            x.write( thing_2)
            x.write('\n')
    x.write( m_type)
    x.write('\n')
    if (m_type == 'sigma'):
        global ar
        global ag
        x.write( 'ag ')
        x.write(ag)
        x.write('\n')
        x.write( 'ar ')
        x.write(ar)
        x.write('\n')
    else:
        #put truth table thing here once working
        placeholder=0
    print ' '
    x.close()
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
