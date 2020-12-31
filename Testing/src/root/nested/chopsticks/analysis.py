
from itertools import product

from root.nested.chopsticks.tree import generate_circle, Node, hands, fingers, start_node

"""Analysis Ideas:
Determining a simple winning/not losing strategy (Complex is done)
Determining a simple strategy that loops the game for ever
Determining a simple losing strategy
"""
# TODO: we changed something about what happens when stalling is allowed, this seems to have changed the stats about this game variant
"""Notes about the game:
Two versions (or more) are possible, one with stalling and one without stalling.
We make the "without stalling" game the default version.
The stalling version simply presents too many options to successfully force a win, which makes it rather uninteresting at present

Of the 225 valid game states, only 192 can be reached from (1,1),(1,1), 194 can be reached with stalling (Unreachable states listed below)
Some like (1,0),(0,0) are not possible because the game should always end with the dead player next up.
Others like (2,1),(4,3) are not possible for unknown reasons. 

A node has no children if and only if the game is over (i.e. there is a winner)

11 levels are needed to display the full tree with 590 nodes (653 nodes with stalling)

There are 14 possible end nodes (i.e. different end states) [This is the 15 valid states minus (0,0),(0,0)]
Every node can either reach every end node, is an end node itself, or is the node (1,0),(4,0).  
This last node is an exception since player 1's only move is to hit the 4 hand with its 1 hand (stalling is not allowed), 
thus it can only end on (0,0),(1,0).  Allowing stalling eliminates this exception.

This is the shortest path (with or without stalling) from the starting ((1,1), (1,1)) node to an end node:
Node(((0, 0), (4, 1))), Node(((4, 1), (3, 0))), Node(((3, 0), (1, 1))), Node(((1, 1), (2, 0))), Node(((1, 1), (1, 1)))

Full breakdown of the shortest path length from a given node to an end node:
length: num of nodes
0: 14
1: 38
2: 93
3: 44
4: 3
The nodes with length 0 to an end node are the end nodes themselves.
The nodes with length 4 are these: Node(((1, 0), (1, 1))), Node(((1, 0), (2, 2))), Node(((1, 1), (1, 1)))
With Stalling:
0: 14
1: 40
2: 93
3: 45
4: 2
The nodes with length 4 are these: Node(((1, 0), (1, 1))), Node(((1, 1), (1, 1)))

There are 3 2-away nodes ("death" nodes) that have no children besides 1-away nodes (i.e. If you are in one of these states, you must go
 to a state which allows the other player to win).  They are (1,0),(4,4), (1,0),(3,0), (1,0),(3,3).  Allowing stalling
 reduces these to just (1,0),(4,4).
The 3 death nodes are children of a combined 13 different nodes (parent death nodes).  These 13 parent death nodes have a
 combined total of 38 unique parent nodes (parent parent death nodes).  Of these 38 parent parent death nodes, only 1 of them,
 (1,0),(1,1), has children who are all parent death nodes, (2,1),(1,0).  Thus if your opponent is in the state (1,0),(1,1), 
 then they will have to go to the state (2,1),(1,0) which allows you to choose to go to the state (1,0),(3,0) which is a death node.
 Thus, your opponent will have to go to (4,0),(1,0), which allows you to win at (0,0),(4,0).  Stalling eliminates this possibility.
Continuing this train of thought back several more moves (~10-12 moves) shows us that the player who starts the game from 
 the typical (1,1),(1,1) node can be forced into losing.  Thus, if the second player plays the game correctly, they can always win.
As before, allowing stalling eliminates the possibility of forcing a win from the beginning.

Using the second player winning strategy, there are approximately 10^6-10^9 different games that could be played.

The 10 nodes which are neither parent nor trap nodes (unclassified nodes) all have at least two children, including at least
 one child which is a parent node and at least one child which is a unclassified node.  None of the children were trap nodes.
"""
# Allow moves which do nothing (e.g. Swapping which hand the fingers are on;  (3,0),(4,1) -> (0,3),(4,1) or (2,1),(4,1) -> (1,2),(4,1))
allow_stall = False

all_nodes = set()
all_values = product(range(0, fingers), repeat=2*hands)
for value in all_values:
    all_nodes.add(Node([[value[i] for i in range(0, hands)], [value[i] for i in range(hands, 2*hands)]]))
print()

linked_list = generate_circle(all_nodes, allow_stall)

# TODO: Try to avoid recursion error by making a non-recursive version
def list_nodes(starting_node, nodes):
    """Determine all nodes which can be reached from starting_node"""
    nodes.add(starting_node)
    for child in linked_list[starting_node]:
        # only explore new nodes
        if child not in nodes:
            list_nodes(child, nodes)

def list_end_nodes(starting_node, nodes, end_nodes):
    """Determine all the end nodes which can be reached from starting_node"""
    nodes.add(starting_node)
    for child in linked_list[starting_node]:
        # If there is a winner, then this child is an end node
        if child.winner() is not None:
            end_nodes.add(child)
        # only explore new nodes
        elif child not in nodes:
            list_end_nodes(child, nodes, end_nodes)

def find_quickest_end(starting_node):
    """Determine the shortest path to the end of a game"""
    hit_nodes = set()
    node_paths = [[starting_node]]
    while True:
        new_node_paths = []
        for node_path in node_paths:
            # if we have an end node, then we are done
            if node_path[0].winner() is not None:
                return node_path
            # otherwise, add a path for each of its child nodes
            else:
                for child in linked_list[node_path[0]]:
                    # only explore new nodes
                    if child not in hit_nodes:
                        hit_nodes.add(child)
                        new_node_paths.append([child, *node_path])
        node_paths = new_node_paths.copy()

def find_trap_nodes(starting_node, find_all=False, log=0):
    # We control parent -> trap
    # They control trap -> parent
    possible_nodes = set()
    list_nodes(starting_node, possible_nodes)
    end_nodes = {node for node in possible_nodes if node.winner() is not None}
    total_parent_nodes = set()
    total_trap_nodes = end_nodes.copy()
    trap_node_list = [end_nodes]

    if log > 1:
        print("Trap 0: " + str(len(end_nodes)) + " " + str(end_nodes))

    i = 0
    # keep going until we run out of trap nodes to find parents of
    while len(trap_node_list[i]) != 0:
        # parent nodes of trap_node_list[i]
        parent_i_nodes = set()
        for node in possible_nodes:
            # parent_i_nodes are any nodes who have at least one child in trap_node_list[i]
            if len(trap_node_list[i] & linked_list[node]) != 0 and node not in total_parent_nodes:
                parent_i_nodes.add(node)
        total_parent_nodes |= parent_i_nodes

        # Nodes 2i+2-away from win node
        trap_i1_nodes = set()
        for node in possible_nodes:
            if node not in total_trap_nodes:
                # nodes whose children are all parent nodes
                overlap = len(total_parent_nodes & linked_list[node])
                if overlap == len(linked_list[node]) and overlap != 0:
                    trap_i1_nodes.add(node)
        total_trap_nodes |= trap_i1_nodes
        trap_node_list.append(trap_i1_nodes.copy())

        if log > 1:
            print("Parent " + str(i) + ": " + str(len(parent_i_nodes)) + " " + str(parent_i_nodes))
            print("Trap " + str(i + 1) + ": " + str(len(trap_i1_nodes)) + " " + str(trap_i1_nodes))
        if starting_node in total_parent_nodes:
            if log:
                print("The first player wins at "+str(i))
            if not find_all:
                break
        if starting_node in total_trap_nodes:
            if log:
                print("The second player wins at "+str(i))
            if not find_all:
                break
        i += 1

    if log:
        print()
        print("Total Parent: " + str(len(total_parent_nodes)) + " " + str(total_parent_nodes))
        print("Total Trap: " + str(len(total_trap_nodes)) + " " + str(total_trap_nodes))
        unclassified_nodes = possible_nodes - (total_parent_nodes | total_trap_nodes)
        print("Remaining Nodes: " + str(len(unclassified_nodes)) + " " + str(unclassified_nodes))
        if log > 1:
            overlap = total_parent_nodes & total_trap_nodes
            print("Parent/Trap Overlap: " + str(len(overlap)) + " " + str(overlap))

    return trap_node_list

def classify_nodes(starting_node, log=0):
    # We control parent -> trap
    # They control trap -> parent
    possible_nodes = set()
    list_nodes(starting_node, possible_nodes)
    end_nodes = {node for node in possible_nodes if node.winner() is not None}
    total_parent_nodes = set()
    total_trap_nodes = end_nodes.copy()
    prev_trap_nodes = end_nodes.copy()

    if log > 1:
        print("Trap 0: " + str(len(end_nodes)) + " " + str(end_nodes))

    i = 0
    # keep going until we run out of trap nodes to find parents of
    while len(prev_trap_nodes) != 0:
        # parent nodes of trap_nodes[i]
        parent_i_nodes = set()
        for node in possible_nodes:
            # parent_i_nodes are any nodes who have at least one child in trap_nodes[i]
            if len(prev_trap_nodes & linked_list[node]) != 0 and node not in total_parent_nodes:
                parent_i_nodes.add(node)
        total_parent_nodes |= parent_i_nodes

        # Nodes 2i+2-away from win node
        trap_i1_nodes = set()
        for node in possible_nodes:
            if node not in total_trap_nodes:
                # nodes whose children are all parent nodes
                overlap = len(total_parent_nodes & linked_list[node])
                if overlap == len(linked_list[node]) and overlap != 0:
                    trap_i1_nodes.add(node)
        total_trap_nodes |= trap_i1_nodes
        prev_trap_nodes = trap_i1_nodes.copy()

        if log > 1:
            print("Parent " + str(i) + ": " + str(len(parent_i_nodes)) + " " + str(parent_i_nodes))
            print("Trap " + str(i + 1) + ": " + str(len(trap_i1_nodes)) + " " + str(trap_i1_nodes))
        if starting_node in total_parent_nodes:
            if log:
                print("The first player wins at "+str(i))
        if starting_node in total_trap_nodes:
            if log:
                print("The second player wins at "+str(i))
        i += 1

    unclassified_nodes = possible_nodes - (total_parent_nodes | total_trap_nodes)
    if log:
        print()
        print("Total Parent: " + str(len(total_parent_nodes)) + " " + str(total_parent_nodes))
        print("Total Trap: " + str(len(total_trap_nodes)) + " " + str(total_trap_nodes))
        print("Remaining Nodes: " + str(len(unclassified_nodes)) + " " + str(unclassified_nodes))
        if log > 1:
            overlap = total_parent_nodes & total_trap_nodes
            print("Parent/Trap Overlap: " + str(len(overlap)) + " " + str(overlap))

    return total_trap_nodes, total_parent_nodes, unclassified_nodes

trap_nodes, parent_nodes, unclassified = classify_nodes(start_node, log=1)

trap_nodes_list = find_trap_nodes(start_node)

# print()
# node_children_classification = {}
# for unknown_node in unclassified:
#     node_children_classification[unknown_node] = {}
#     for un_child in linked_list[unknown_node]:
#         if un_child in unclassified:
#             node_children_classification[unknown_node][un_child] = "Unclassified"
#         if un_child in parent_nodes:
#             node_children_classification[unknown_node][un_child] = "Parent"
#         if un_child in trap_nodes:
#             node_children_classification[unknown_node][un_child] = "Trap"
#     print(repr(unknown_node)+": "+str(node_children_classification[unknown_node]))


""" Impossible States (w/o Stalling)(Turn: 0):
(0, 0), (0, 0)
(1, 0), (0, 0)
(1, 1), (0, 0)
(1, 1), (4, 3)
(1, 1), (4, 4)
(2, 0), (0, 0)
(2, 1), (0, 0)
(2, 1), (4, 3)
(2, 1), (4, 4)
(2, 2), (0, 0)
(2, 2), (4, 3)
(2, 2), (4, 4)
(3, 0), (0, 0)
(3, 1), (0, 0)
(3, 1), (4, 3)
(3, 1), (4, 4)
(3, 2), (0, 0)
(3, 2), (4, 3)
(3, 2), (4, 4)
(3, 3), (0, 0)
(3, 3), (4, 3)
(3, 3), (4, 4)
(4, 0), (0, 0)
(4, 1), (0, 0)
(4, 1), (4, 4)
(4, 2), (0, 0)
(4, 2), (4, 4)
(4, 3), (0, 0)
(4, 3), (4, 0)
(4, 3), (4, 4)
(4, 4), (0, 0)
(4, 4), (4, 0)
(4, 4), (4, 4)
"""
""" Impossible States (w/ Stalling)(Turn: 0):
(0, 0), (0, 0)
(1, 0), (0, 0)
(1, 1), (0, 0)
(1, 1), (4, 3)
(1, 1), (4, 4)
(2, 0), (0, 0)
(2, 1), (0, 0)
(2, 1), (4, 3)
(2, 1), (4, 4)
(2, 2), (0, 0)
(2, 2), (4, 3)
(2, 2), (4, 4)
(3, 0), (0, 0)
(3, 1), (0, 0)
(3, 1), (4, 3)
(3, 1), (4, 4)
(3, 2), (0, 0)
(3, 2), (4, 3)
(3, 2), (4, 4)
(3, 3), (0, 0)
(3, 3), (4, 3)
(3, 3), (4, 4)
(4, 0), (0, 0)
(4, 1), (0, 0)
(4, 1), (4, 4)
(4, 2), (0, 0)
(4, 2), (4, 4)
(4, 3), (0, 0)
(4, 3), (4, 4)
(4, 4), (0, 0)
(4, 4), (4, 4)
"""
""" States added by stalling (Turn: 0):
(4, 3), (4, 0)
(4, 4), (4, 0)
"""
