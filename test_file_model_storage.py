nodes = {}
key_with_partners = {}
m_type = 'no'
ar = -1
ag = -1

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





try_open = open_old_model('format_old_model')
print try_open
assign_all_things(try_open)
print nodes
print key_with_partners
print m_type
print ag
print ar
file_output_model('test_run_model_out')
