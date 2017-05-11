import matplotlib.pyplot as plt

test_run = {1:[0,1], 2:[0,1], 3:[1,1], 4:[0,0], 5:[1,1], 6:[0,0], 7:[1,1], 8:[0,0], 9:[1,1], 10:[0,0], 11:[1,1]}
node_names = ['a', 'b']

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

split_node_history_and_graph(test_run)
