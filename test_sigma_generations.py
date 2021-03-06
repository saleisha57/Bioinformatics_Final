import networkx as nx
import matplotlib.pyplot as plt
#just testing functions using these, don't need other libraries right now

#global variables for model
#still need:  nodes, buddies, etc that are all called multiple times
#maybe a 'model type' variable for truth table vs. sigma type update schemes
current_state = []
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
        print key
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
                graph.add_edge(key,sub_key[0:len(sub_key) - 1], color = 'g')
            else:
                graph.add_edge(key,sub_key[0:len(sub_key) - 1], color = 'r')
    return graph

#PUT TRUTH TABLE MAKING HERE

def set_model_type():
    global m_type
    m_type_hold = raw_input("Enter model type (Must be 'sigma' or 'ttable'): ")
    m_type = m_type_hold
    if m_type == 'sigma':
        global ar
        global ag
        ar_n = raw_input("Enter ar value: ")
        ag_n = raw_input("Enter ag value: ")
        ag = ag_n
        ar = ar_n
    else:
        placeholder = 0
        #put t table stuff here

def draw_the_graph(y):
        edges = y.edges()
        pos = nx.circular_layout(y)
        colors = [y[u][v]['color'] for u,v in edges]
        nx.draw(y, pos, edges=edges, edge_color=colors, with_labels = True)
        name = 'graph_of_nodes'
        plt.show()
        plt.savefig(name)
        plt.close()

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
        #Need to manually save graph as you go along
        plt.show()

def assign_all_things(read_stuff_list):
    #assigns main nodes, edges out of node
    global nodes
    global key_with_partners
    global node_names
    node_names_hold = []
    for thing in range(len(read_stuff_list[0])):
        nodes[read_stuff_list[0][thing]] = read_stuff_list[thing + 1]
        node_names_hold.append(read_stuff_list[0][thing])
        #key_with_partners[read_stuff_list[0][thing]] = read_stuff_list[thing + len(read_stuff_list[0]) + 1]
    location_model_type = len(read_stuff_list[0]) * 2 + 1
    #print location_model_type
    node_names_hold.sort()
    node_names = node_names_hold
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
    global node_names
    global key_with_partners
    global m_type
    for thing in node_names:
        x.write( thing+ " ")
    x.write( "\n")
    for thing in node_names:
        for thing_2 in nodes[thing]:
            x.write( thing_2 + " "),
        x.write('\n')
    # for thing in node_names:
    #     for thing_2 in key_with_partners[thing]:
    #         x.write( thing_2+ " "),
    #     x.write('\n')
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

#find all the nodes which point to a given node, saves interaction type
def find_all_nodes_with_point_to_a_node():
    global nodes
    global key_with_partners
    give_back_list_friends={}
    for thing_outer in nodes:
        search_node = thing_outer
        give_back_list_friends[search_node] = []
        for thing in nodes:
            #print 'in first for', thing
            for thing_2 in nodes[thing]:
                #print 'in second for', thing_2
                if search_node == thing_2[0:len(thing_2) - 1]:
                    give_back_list_friends[search_node].append(thing + thing_2[len(thing_2)-1:len(thing_2)])
    key_with_partners = give_back_list_friends

#does a signma update scheme
def sigma_function_new_value(value_old, c_state, target):
    #print 'inside sigma function'
    sum_val = 0
    global ar
    global ag
    global nodes
    global key_with_partners
    global node_names
    thing = target
    #global current_state
    for thing_2 in key_with_partners[thing]:
        #print 'on box', thing_2
        print thing_2, 'inside'
        if thing_2[len(thing_2) - 1:len(thing_2)] == '+':
            print 'entered the plus one'
            #print current_state[node_names.index(thing_2[0:len(thing_2) -1])], 'value in current_state'
            #print int(ag) * int(current_state[node_names.index(thing_2[0:len(thing_2) -1])]), 'times '
            sum_val = sum_val + int(ag) * int(c_state[node_names.index(thing_2[0:len(thing_2) -1])])
            #print sum_val, sum_val
            #print sum_val
            #print 'entered'
        elif thing_2[len(thing_2)-1:len(thing_2)] == '-':
            sum_val = sum_val + int(ar) * int(c_state[node_names.index(thing_2[0:len(thing_2)-1])])
        else:
            sum_val = 0
    #print sum_val, 'after updates'
    if sum_val > 0:
        #print 'tis true greater than'
        return_val = 1
    elif sum_val < 0:
        #print 'tis true less than'
        return_val = 0
    else:
        #print 'u shouldnt b here rn if first round'
        return_val = value_old
    #print return_val, 'new from sigma'
    return return_val

#runs a single generation update
#problem is in HERE
def run_a_generation_sigma(generaton_numb, c_state):
    #print 'inside run one generation'
    #print past_states_r
    #now update
    global node_names
    hold_states = []
    for i in range(len(node_names)):
        current_value_store = c_state[i]
        print 'current value', c_state[i]
        #print 'current state for node', i, 'is', current_value_store
        #print sigma_function_new_value(current_value_store), 'actually got from sigma'
        new_val = sigma_function_new_value(current_value_store, c_state, node_names[i])
        if c_state[i] == 2:
            new_val = 2
        hold_states.append(new_val)
        #print hold_states, 'hold states'
    #print hold_states, 'hold states has'
    print hold_states
    return hold_states
    #print 'hold states', hold_states, 'current_state', current_state

def run_set_number_generations_sigma(number, initial_values):
    #print 'inside main function'
    past_states_r = {}
    past_states_r[0] = initial_values
    print past_states_r
    c_state = initial_values
    for i in range(1, number):
        #print current_state
        print 'generation ', i
        print 'current state is:', c_state
        b = run_a_generation_sigma(i, c_state)
        print b, 'b'
        c_state = b
        #add in shut offs here
        past_states_r[i] = c_state
    global past_states
    past_states=  past_states_r


get_edges()
set_model_type()
find_all_nodes_with_point_to_a_node()
print node_names
for thing in node_names:
    print 'on node', thing
    print 'points too', nodes[thing]
    print 'pointed too by ', key_with_partners[thing]
    print '\n'

# run_set_number_generations_sigma(16, [0,0,0,0,0,0,0,0,1,0,0,0,0,0])
# for i in range(len(past_states)):
#     print 'generation', i
#     for j in range(len(past_states[i])):
#         print node_names[j], 'state', past_states[i][j]
# y = translate_to_graph()
# draw_the_graph(y)
# split_node_history_and_graph(past_states)
