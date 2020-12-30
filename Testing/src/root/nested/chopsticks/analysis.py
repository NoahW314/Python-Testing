
from itertools import product
from typing import List, Any

from root.nested.chopsticks.tree import generate_circle, Node, generate_tree, Tree

"""Analysis Ideas:
Determining a simple winning/not losing strategy
Determining a simple strategy that loops the game for ever
Determining a simple losing strategy
"""

"""Notes about the game:
Two versions (or more) are possible, one with stalling and one without stalling.
We make the "without stalling" game the default version.

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
 the typical (1,1),(1,1) node can be forced into losing.  Thus, if the second player plays the game correctly, they can always win.v
As before, allowing stalling eliminates the possibility of forcing a win from the beginning.

Using the second player winning strategy, there are approximately 10^6-10^9 different games that could be played.
"""
# Allow moves which do nothing (e.g. Swapping which hand the fingers are on;  (3,0),(4,1) -> (0,3),(4,1) or (2,1),(4,1) -> (1,2),(4,1))
allow_stall = False

# levels = 12
# tree = generate_tree(Tree(Node(((1,1),(1,1)))), levels, turn=0, max_depth=levels, env_size=(1000, 1000), allow_stall=allow_stall)
# tree_nodes = set()
# for node_level in tree.nodes:
#     for node in node_level:
#         tree_nodes.add(node)
all_nodes = set()
all_values = product(range(0, 5), repeat=4)
for value in all_values:
    all_nodes.add(Node([[value[0], value[1]], [value[2], value[3]]]))
# print(len(all_nodes))
# print(all_nodes)
print()

linked_list = generate_circle(all_nodes, allow_stall)
possible_nodes = set()

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


list_nodes(Node(((1,1), (1,1))), possible_nodes)
path = find_quickest_end(Node(((1,1), (1,1))))
# print(path)
# Classify all the nodes by how quickly they can reach an end node
dist_to_end = {}
for node in possible_nodes:
    # ignore the starting node
    path = find_quickest_end(node)[:-1]
    if len(path) not in dist_to_end.keys():
        dist_to_end[len(path)] = []
    dist_to_end[len(path)].append(node)
# for length, node_list in dist_to_end.items():
#     print(str(length)+": "+str(len(node_list)))
# print(dist_to_end[4])
survival_nodes = {}
# the 2-away nodes from which have only 1-away nodes as children
death_nodes = set()
for node in dist_to_end[2]:
    # go through each 2 away node and record the children which are not 1 away nodes
    survival_nodes[node] = [n for n in linked_list[node] if n not in dist_to_end[1]]
    if len(survival_nodes[node]) == 0:
        death_nodes.add(node)
# who are the parents of the death_nodes
parent_death_nodes = set()
# the set of all nodes whose only children are parent death nodes
only_parent_death_child_nodes = set()
# print(death_nodes)
for node in possible_nodes:
    if len(death_nodes & linked_list[node]) != 0:
        parent_death_nodes.add(node)
for node in possible_nodes:
    if len(parent_death_nodes & linked_list[node]) != 0:
        # if all the children of this node are parent death nodes, then add it to the set
        if len(parent_death_nodes & linked_list[node]) == len(linked_list[node]):
            only_parent_death_child_nodes.add(node)
# print(len(parent_death_nodes))
# print(parent_death_nodes)
# print(len(parent_parent_death_nodes))
# print(parent_parent_death_nodes)
# print(len(only_parent_death_child_nodes))
# print(only_parent_death_child_nodes)
# child_parent_death_nodes = linked_list[only_parent_death_child_nodes.pop()].copy()
# print(child_parent_death_nodes)
# trap_death_nodesq = linked_list[child_parent_death_nodes.pop()].copy()
# print(trap_death_nodesq)
print()
# Work backwards from (1,0),(1,1)
# It is your opponent's turn in (1,0),(1,1)
# We control parent -> trap
# They control trap -> parent
print()
# child_node = Node(((1,0),(1,1)))
# just_above_win = set(dist_to_end[1])
# # Nodes 2-away from our win end nodes (win node(s) from here on out)
# trap_0_nodes = death_nodes.copy()
# parent_0_nodes = parent_death_nodes.copy()
# # Nodes 4-away from win node
# trap_1_nodes = {child_node}
# total_parent_nodes = just_above_win | parent_0_nodes
# total_trap_nodes = trap_0_nodes | trap_1_nodes
# # parent nodes of trap_1_nodes
# parent_1_nodes = set()
# for node in possible_nodes:
#     # parent_1_nodes are any nodes who have at least one child in trap_1_nodes
#     if len(trap_1_nodes & linked_list[node]) != 0 and node not in total_parent_nodes:
#         parent_1_nodes.add(node)
# total_parent_nodes |= parent_1_nodes
#
# # Nodes 6-away from win node
# trap_2_nodes = set()
# for node in possible_nodes:
#     if node not in total_trap_nodes:
#         # nodes whose children are all parent nodes
#         overlap = len(total_parent_nodes & linked_list[node])
#         if overlap == len(linked_list[node]) and overlap != 0:
#             trap_2_nodes.add(node)
# total_trap_nodes |= trap_2_nodes
#
# # parent nodes of trap_2_nodes
# parent_2_nodes = set()
# for node in possible_nodes:
#     # parent_2_nodes are any nodes who have at least one child in trap_2_nodes
#     if len(trap_2_nodes & linked_list[node]) != 0 and node not in total_parent_nodes:
#         parent_2_nodes.add(node)
# total_parent_nodes |= parent_2_nodes
#
# # Nodes 8-away from win node
# trap_3_nodes = set()
# for node in possible_nodes:
#     if node not in total_trap_nodes:
#         # nodes whose children are all in parent_2_nodes
#         overlap = len(total_parent_nodes & linked_list[node])
#         if overlap == len(linked_list[node]) and overlap != 0:
#             trap_3_nodes.add(node)
# total_trap_nodes |= trap_3_nodes
#
# # parent nodes of trap_3_nodes
# parent_3_nodes = set()
# for node in possible_nodes:
#     # parent_3_nodes are any nodes who have at least one child in trap_3_nodes
#     if len(trap_3_nodes & linked_list[node]) != 0 and node not in total_parent_nodes:
#         parent_3_nodes.add(node)
# total_parent_nodes |= parent_3_nodes
#
# # Nodes 10-away from win node
# trap_4_nodes = set()
# for node in possible_nodes:
#     if node not in total_trap_nodes:
#         # nodes whose children are all in parent_3_nodes
#         overlap = len(total_parent_nodes & linked_list[node])
#         if overlap == len(linked_list[node]) and overlap != 0:
#             trap_4_nodes.add(node)
# total_trap_nodes |= trap_4_nodes
#
# # parent nodes of trap_4_nodes
# parent_4_nodes = set()
# for node in possible_nodes:
#     # parent_4_nodes are any nodes who have at least one child in trap_4_nodes
#     if len(trap_4_nodes & linked_list[node]) != 0 and node not in total_parent_nodes:
#         parent_4_nodes.add(node)
# total_parent_nodes |= parent_4_nodes
#
# # Nodes 12-away from win node
# trap_5_nodes = set()
# for node in possible_nodes:
#     if node not in total_trap_nodes:
#         # nodes whose children are all in parent_4_nodes
#         overlap = len(total_parent_nodes & linked_list[node])
#         if overlap == len(linked_list[node]) and overlap != 0:
#             trap_5_nodes.add(node)
# total_trap_nodes |= trap_5_nodes
#
# print("Parent -1: "+str(len(just_above_win))+" "+str(just_above_win))
# print("Trap 0: "+str(len(trap_0_nodes))+" "+str(trap_0_nodes))
# print("Parent 0: "+str(len(parent_0_nodes))+" "+str(parent_0_nodes))
# print("Trap 1: "+str(len(trap_1_nodes))+" "+str(trap_1_nodes))
# print("Parent 1: "+str(len(parent_1_nodes))+" "+str(parent_1_nodes))
# print("Trap 2: "+str(len(trap_2_nodes))+" "+str(trap_2_nodes))
# print("Parent 2: "+str(len(parent_2_nodes))+" "+str(parent_2_nodes))
# print("Trap 3: "+str(len(trap_3_nodes))+" "+str(trap_3_nodes))
# print("Parent 3: "+str(len(parent_3_nodes))+" "+str(parent_3_nodes))
# print("Trap 4: "+str(len(trap_4_nodes))+" "+str(trap_4_nodes))
# print("Parent 4: "+str(len(parent_4_nodes))+" "+str(parent_4_nodes))
# print("Trap 5: "+str(len(trap_5_nodes))+" "+str(trap_5_nodes))
# print()
# print("Total Parent: "+str(len(total_parent_nodes))+" "+str(total_parent_nodes))
# print("Total Trap: "+str(len(total_trap_nodes))+" "+str(total_trap_nodes))
# overlap = total_parent_nodes & total_trap_nodes
# print("Parent/Trap Overlap: "+str(len(overlap))+" "+str(overlap))


just_above_win = set(dist_to_end[1])
end_nodes = set(dist_to_end[0])
# Nodes 2-away from our win end nodes (win node(s) from here on out)
trap_0_nodes = death_nodes.copy()
parent_0_nodes = parent_death_nodes.copy()
# Nodes 4-away from win node
trap_1_nodes = {Node(((1,0),(1,1)))}
total_parent_nodes = just_above_win | parent_0_nodes
total_trap_nodes = end_nodes | trap_0_nodes | trap_1_nodes
parent_nodes = [parent_0_nodes]
trap_nodes = [trap_0_nodes, trap_1_nodes]

print("Trap -1: "+str(len(end_nodes))+" "+str(end_nodes))
print("Parent -1: "+str(len(just_above_win))+" "+str(just_above_win))
print("Trap 0: "+str(len(trap_0_nodes))+" "+str(trap_0_nodes))
print("Parent 0: "+str(len(parent_0_nodes))+" "+str(parent_0_nodes))
print("Trap 1: "+str(len(trap_1_nodes))+" "+str(trap_1_nodes))

number_of_times = 15
for i in range(1, number_of_times+1):
    # parent nodes of trap_nodes[i]
    parent_i_nodes = set()
    for node in possible_nodes:
        # parent_i_nodes are any nodes who have at least one child in trap_nodes[i]
        if len(trap_nodes[i] & linked_list[node]) != 0 and node not in total_parent_nodes:
            parent_i_nodes.add(node)
    total_parent_nodes |= parent_i_nodes
    parent_nodes.append(parent_i_nodes.copy())

    # Nodes 2i+4-away from win node
    trap_i1_nodes = set()
    for node in possible_nodes:
        if node not in total_trap_nodes:
            # nodes whose children are all parent nodes
            overlap = len(total_parent_nodes & linked_list[node])
            if overlap == len(linked_list[node]) and overlap != 0:
                trap_i1_nodes.add(node)
    total_trap_nodes |= trap_i1_nodes
    trap_nodes.append(trap_i1_nodes.copy())

    print("Parent " + str(i) + ": " + str(len(parent_i_nodes)) + " " + str(parent_i_nodes))
    print("Trap " + str(i+1) + ": " + str(len(trap_i1_nodes)) + " " + str(trap_i1_nodes))
    end = False
    if Node(((1,1), (1,1))) in total_parent_nodes:
        print("We are at the start!!!")
        end = True
    if Node(((1,1), (1,1))) in total_trap_nodes:
        print("We are trapped?!?!")
        end = False
    if end:
        break

print()
print("Total Parent: "+str(len(total_parent_nodes))+" "+str(total_parent_nodes))
print("Total Trap: "+str(len(total_trap_nodes))+" "+str(total_trap_nodes))
unclassified_nodes = possible_nodes - (total_parent_nodes | total_trap_nodes)
print("Remaining Nodes: "+str(len(unclassified_nodes))+" "+str(unclassified_nodes))
overlap = total_parent_nodes & total_trap_nodes
print("Parent/Trap Overlap: "+str(len(overlap))+" "+str(overlap))

# Question: can you force your opponent into losing?
# Question: Can your opponent always avoid the 2-away "death" nodes?
# If your opponent can always avoid getting into a 2-away node which has no survival nodes, then you can't force a win
# Otherwise, more exploration is required



# all_end_nodes = {node for node in possible_nodes if node.winner() is not None}
# nodes_to_end_nodes = {}
# for node in possible_nodes:
#     node_end_nodes = set()
#     node_all_nodes = set()
#     list_end_nodes(node, node_all_nodes, node_end_nodes)
#     nodes_to_end_nodes[node] = node_end_nodes
# print()
# impossible_nodes = sorted(all_nodes-possible_nodes)
# print(len(impossible_nodes))
# for node in impossible_nodes:
#     print(repr(node)[6:-2])

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
